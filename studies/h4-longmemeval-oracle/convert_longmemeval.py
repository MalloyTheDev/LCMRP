#!/usr/bin/env python3
"""Convert a LongMemEval file into CorpusStudio `instruction` JSONL.

Target: the H4-Oracle study (see README.md). This produces rows the
CorpusStudio eval harness can consume directly:

    corpus-studio eval-run out.jsonl instruction --model ... --backend ...

Each output row is:
    {"instruction": <question>, "input": <evidence context>,
     "output": <gold answer>, "tags": [<question_type>, ...]}

The CorpusStudio eval pipeline builds the prompt as
`instruction + "\\n\\nInput:\\n" + input` and treats `output` as the reference
answer, so the model sees the question plus the supplied memory context and the
scorer compares its answer to `output`. Per-`question_type` accuracy comes for
free via the harness `tag_summary`.

LongMemEval schema assumed (verify against the actual release before a real
run): a JSON list of items, each with `question_id`, `question_type`,
`question`, `answer`, optional `question_date`, and `haystack_sessions`
(a list of sessions, each a list of turns `{"role", "content"}`). In the
`_oracle` file the haystack already contains only evidence sessions; if
`answer_session_ids` + `haystack_session_ids` are present we intersect to be
safe. Abstention items (`question_id` ending in `_abs`) are tagged `abstention`.

Deterministic, stdlib only. Run `--selftest` to validate on a synthetic item
without the real dataset.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def _render_session(session: list[dict[str, Any]], date: str | None) -> str:
    lines: list[str] = []
    if date:
        lines.append(f"[session date: {date}]")
    for turn in session:
        role = str(turn.get("role", "?"))
        content = str(turn.get("content", "")).strip()
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def _evidence_sessions(item: dict[str, Any]) -> list[tuple[list[dict], str | None]]:
    """Return (session, date) pairs that are evidence for the answer.

    Oracle files already contain only evidence sessions, so the default is
    "use every haystack session". If explicit answer/haystack session ids are
    present we keep only the answer sessions (defensive for non-oracle files).
    """
    sessions = item.get("haystack_sessions") or []
    dates = item.get("haystack_dates") or [None] * len(sessions)
    ids = item.get("haystack_session_ids")
    answer_ids = item.get("answer_session_ids")
    pairs = list(zip(sessions, dates))
    if ids and answer_ids:
        keep = set(answer_ids)
        pairs = [(s, d) for s, d, sid in zip(sessions, dates, ids) if sid in keep]
    return pairs


def convert_item(item: dict[str, Any]) -> dict[str, Any]:
    question = str(item["question"]).strip()
    answer = str(item["answer"]).strip()
    qtype = str(item.get("question_type", "unknown"))
    qid = str(item.get("question_id", ""))

    evidence = _evidence_sessions(item)
    context = "\n\n".join(_render_session(s, d) for s, d in evidence)

    instruction = question
    qdate = item.get("question_date")
    if qdate:
        instruction = f"{question}\n(Question asked on: {qdate})"

    tags = [qtype]
    if qid.endswith("_abs"):
        tags.append("abstention")

    return {
        "instruction": instruction,
        "input": context,
        "output": answer,
        "tags": tags,
    }


def convert(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [convert_item(it) for it in items]


def _write_jsonl(rows: list[dict[str, Any]], out) -> None:
    for row in rows:
        out.write(json.dumps(row, ensure_ascii=False) + "\n")


SYNTHETIC = [
    {
        "question_id": "kv_001",
        "question_type": "knowledge-update",
        "question": "What city do I live in now?",
        "answer": "Denver",
        "question_date": "2026-05-01",
        "haystack_session_ids": ["s1", "s2", "s3"],
        "answer_session_ids": ["s1", "s3"],
        "haystack_dates": ["2025-01-10", "2025-06-02", "2026-04-20"],
        "haystack_sessions": [
            [{"role": "user", "content": "I just moved to Boston."}],
            [{"role": "user", "content": "The weather is nice today."}],
            [{"role": "user", "content": "Update: I relocated to Denver last week."}],
        ],
    },
    {
        "question_id": "sp_002_abs",
        "question_type": "single-session-preference",
        "question": "What is my favorite fruit?",
        "answer": "The information is not available.",
        "haystack_sessions": [
            [{"role": "user", "content": "I had a busy day at work."}],
        ],
    },
]


def _selftest() -> int:
    rows = convert(SYNTHETIC)
    assert len(rows) == 2, rows
    # Item 1: only evidence sessions s1 and s3 are kept (s2 dropped).
    r0 = rows[0]
    assert set(r0) == {"instruction", "input", "output", "tags"}, r0
    assert r0["output"] == "Denver"
    assert "moved to Boston" in r0["input"] and "relocated to Denver" in r0["input"]
    assert "weather is nice" not in r0["input"], "non-evidence session leaked"
    assert r0["tags"] == ["knowledge-update"]
    assert "2026-05-01" in r0["instruction"]
    # Item 2: abstention tag added, all sessions used (no ids given).
    r1 = rows[1]
    assert r1["tags"] == ["single-session-preference", "abstention"], r1["tags"]
    # Every row is valid JSON and non-empty on required fields.
    for r in rows:
        json.dumps(r)
        assert r["instruction"] and r["output"]
    print("selftest OK: 2 items converted, evidence-only context, tags correct")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", nargs="?", help="LongMemEval JSON file (list of items)")
    ap.add_argument("-o", "--output", help="output instruction JSONL (default stdout)")
    ap.add_argument("--selftest", action="store_true", help="run the synthetic self-test and exit")
    ap.add_argument("--max-input-chars", type=int, default=0,
                    help="warn (to stderr) if a row's rendered context exceeds this many chars")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    if not args.input:
        ap.error("input file required (or use --selftest)")

    with open(args.input, encoding="utf-8") as f:
        items = json.load(f)
    if not isinstance(items, list):
        ap.error("expected a JSON list of LongMemEval items")

    rows = convert(items)

    if args.max_input_chars:
        for row, it in zip(rows, items):
            n = len(row["input"])
            if n > args.max_input_chars:
                print(f"WARN {it.get('question_id','?')}: context {n} chars "
                      f"(> {args.max_input_chars}); may exceed the seq budget",
                      file=sys.stderr)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out:
            _write_jsonl(rows, out)
    else:
        _write_jsonl(rows, sys.stdout)
    print(f"converted {len(rows)} items", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
