"""Adversarial structural gates for the M1 Layer 1 launch package.

These tests deliberately inspect only the four M1 launch documents.  They do
not decide whether a taxonomy is scientifically correct, novel, validated, or
complete.  They test whether the launch package exposes enough structure to be
falsifiable and whether it preserves the program's claim and product-independence
boundaries.  Named-section and structured-item thresholds can reject an
equivalent but differently organized document (a known false-positive risk),
while regular-expression claim checks can miss indirect rhetoric (a known
false-negative risk).  The independent review therefore pairs these mechanical
gates with a prose read and the repository-wide validator.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]

FOUNDATION = "docs/program/M1_FOUNDATION.md"
PRIOR_ART = "docs/taxonomy/M1_PRIOR_ART_AND_COMPETING_TAXONOMIES.md"
TAXONOMY = "docs/taxonomy/MEMORY_TAXONOMY_v0.1.md"
FORMAL_MODEL = "docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md"
LAUNCH_PATHS = (FOUNDATION, PRIOR_ART, TAXONOMY, FORMAL_MODEL)

LAYER_DECLARATION = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?"
    r"(?:applicable\s+|research\s+)?layer(?:\*\*)?\s*:\s*"
    r"(?:\*\*)?(.+?)(?:\*\*)?\s*$",
    re.IGNORECASE,
)
STATUS_DECLARATION = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?"
    r"(?:(?:m1|launch|milestone)\s+)?(?:status|state)(?:\*\*)?\s*:\s*"
    r"(?:\*\*)?(.+?)(?:\*\*)?\s*$",
    re.IGNORECASE,
)

MECHANISM_EVIDENCE_LABELS = {
    "HYPOTHESIS",
    "PROTOTYPE",
    "REPLICATED",
    "BENCHMARKED",
    "ROBUSTNESS-TESTED",
    "SECURITY-REVIEWED",
    "INDEPENDENTLY VALIDATED",
    "INTEGRATION CANDIDATE",
    "PRODUCTION-READY",
}


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    line_index: int


def _without_fenced_code(text: str) -> str:
    """Remove fenced blocks so examples cannot satisfy or trip prose gates."""

    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(```+|~~~+)", line)
        if marker:
            current = marker.group(1)[0]
            if fence is None:
                fence = current
            elif fence == current:
                fence = None
            continue
        if fence is None:
            kept.append(line)
    return "\n".join(kept)


def _plain_heading_title(title: str) -> str:
    title = re.sub(r"\s+#+\s*$", "", title.strip())
    title = re.sub(r"[*_`]+", "", title)
    return re.sub(r"\s+", " ", title).strip()


def _plain_metadata_line(line: str) -> str:
    """Ignore Markdown emphasis around metadata keys without weakening values."""

    return re.sub(r"[*_`]", "", line)


def _headings(text: str) -> list[Heading]:
    result: list[Heading] = []
    fence: str | None = None
    for index, line in enumerate(text.splitlines()):
        marker = re.match(r"^\s*(```+|~~~+)", line)
        if marker:
            current = marker.group(1)[0]
            if fence is None:
                fence = current
            elif fence == current:
                fence = None
            continue
        if fence is not None:
            continue
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            result.append(
                Heading(len(match.group(1)), _plain_heading_title(match.group(2)), index)
            )
    return result


def _find_section(text: str, *title_patterns: str) -> tuple[Heading, str] | None:
    lines = text.splitlines()
    headings = _headings(text)
    for position, heading in enumerate(headings):
        if not any(re.search(pattern, heading.title, re.IGNORECASE) for pattern in title_patterns):
            continue
        end = len(lines)
        for later in headings[position + 1 :]:
            if later.level <= heading.level:
                end = later.line_index
                break
        return heading, "\n".join(lines[heading.line_index + 1 : end]).strip()
    return None


def _table_data_rows(text: str) -> int:
    lines = text.splitlines()
    count = 0
    in_table = False
    for index, line in enumerate(lines):
        if "|" not in line:
            in_table = False
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            in_table = False
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            in_table = True
            continue
        if in_table:
            count += 1
        elif index + 1 < len(lines):
            next_cells = [
                cell.strip()
                for cell in lines[index + 1].strip().strip("|").split("|")
            ]
            in_table = len(next_cells) >= 2 and all(
                re.fullmatch(r":?-{3,}:?", cell) for cell in next_cells
            )
    return count


def _structured_items(text: str) -> int:
    bullets = sum(
        1
        for line in text.splitlines()
        if re.match(r"^\s*(?:[-+*]|\d+[.)])\s+\S", line)
    )
    definitions = sum(
        1
        for line in text.splitlines()
        if re.match(r"^\s*\*\*[^*]+\*\*\s*(?::|[—–-])\s+\S", line)
    )
    transitions = len(re.findall(r"(?:->|→)", _without_fenced_code(text)))
    return max(bullets + definitions, _table_data_rows(text), transitions)


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", _without_fenced_code(text)))


def _github_slug(title: str) -> str:
    slug = _plain_heading_title(title).lower()
    slug = re.sub(r"[^\w\- ]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    return re.sub(r"-+", "-", slug)


class M1LaunchAdversarialTests(unittest.TestCase):
    """Fail closed on missing launch artifacts and unsafe launch claims."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.paths = {relative: ROOT / relative for relative in LAUNCH_PATHS}
        cls.docs = {
            relative: path.read_text(encoding="utf-8") if path.is_file() else ""
            for relative, path in cls.paths.items()
        }

    def _doc(self, relative: str) -> str:
        self.assertTrue(
            self.paths[relative].is_file(),
            f"required M1 launch artifact is missing: {relative}",
        )
        text = self.docs[relative]
        self.assertTrue(text.strip(), f"required M1 launch artifact is empty: {relative}")
        return text

    def _required_section(
        self,
        relative: str,
        *patterns: str,
        min_words: int = 20,
    ) -> str:
        text = self._doc(relative)
        found = _find_section(text, *patterns)
        self.assertIsNotNone(
            found,
            f"{relative} needs a named section matching one of: {patterns}",
        )
        assert found is not None
        heading, body = found
        self.assertGreaterEqual(
            _word_count(body),
            min_words,
            f"section '{heading.title}' in {relative} is not substantive",
        )
        return body

    def test_01_launch_package_is_present(self) -> None:
        missing = [relative for relative, path in self.paths.items() if not path.is_file()]
        self.assertEqual([], missing, f"missing M1 launch artifacts: {missing}")

    def test_02_every_artifact_declares_exactly_layer_1(self) -> None:
        for relative in LAUNCH_PATHS:
            with self.subTest(document=relative):
                declarations = [
                    match.group(1).strip()
                    for line in self._doc(relative).splitlines()
                    if (match := LAYER_DECLARATION.match(_plain_metadata_line(line)))
                ]
                self.assertEqual(
                    1,
                    len(declarations),
                    f"{relative} must contain exactly one explicit layer declaration",
                )
                self.assertRegex(
                    declarations[0],
                    r"(?i)^(?:layer\s*)?1\b\s*(?:[—–:-]\s*)?foundational research\.?$",
                    f"{relative} must declare Layer 1 — Foundational Research",
                )

    def test_03_m1_is_launched_but_not_complete(self) -> None:
        foundation = self._doc(FOUNDATION)
        declarations = [
            match.group(1).strip()
            for line in foundation.splitlines()
            if (match := STATUS_DECLARATION.match(_plain_metadata_line(line)))
        ]
        self.assertEqual(1, len(declarations), "M1 foundation needs one launch status")
        self.assertRegex(
            declarations[0],
            r"(?i)^(?:launch(?:ed)? candidate|launched|active|in[ -]progress)"
            r"(?:\s*[—–:-].*)?$",
            "M1 status must be a launch candidate, LAUNCHED, ACTIVE, or IN PROGRESS",
        )

        false_completion = re.compile(
            r"(?i)(?:\bm1\s+(?:is|was|has been)\s+(?:now\s+)?"
            r"(?:complete|completed|finished|closed)\b|"
            r"\b(?:m1\s+)?status\s*:\s*(?:complete|completed|finished|closed)\b)"
        )
        for relative in LAUNCH_PATHS:
            with self.subTest(document=relative):
                self.assertIsNone(
                    false_completion.search(_without_fenced_code(self._doc(relative))),
                    f"{relative} falsely represents M1 as complete",
                )


    def test_04_m1_foundation_exit_and_stop_criteria_remain_open_and_actionable(self) -> None:
        foundation = self._doc(FOUNDATION)

        def assert_exit_and_stop_criteria_are_valid(document: str, *, label: str) -> None:
            exit_section = _find_section(
                document,
                r"^exit criteria$",
                r"^launch exit criteria$",
                r"^m1 exit criteria$",
            )
            self.assertIsNotNone(
                exit_section,
                f"{label} needs an exit-criteria section",
            )
            assert exit_section is not None
            exit_heading, exit_body = exit_section
            exit_prose = _without_fenced_code(exit_body)
            unchecked_exit_items = re.findall(r"(?im)^\s*-\s*\[ \]\s+\S.*$", exit_prose)
            checked_exit_items = re.findall(r"(?im)^\s*-\s*\[[xX]\]\s+\S.*$", exit_prose)
            all_exit_items = unchecked_exit_items + checked_exit_items
            self.assertGreaterEqual(
                _word_count(exit_body),
                40,
                f"section '{exit_heading.title}' in {label} is not substantive",
            )
            self.assertGreaterEqual(
                len(unchecked_exit_items),
                2,
                f"section '{exit_heading.title}' in {label} must list multiple unchecked exit criteria",
            )
            self.assertGreaterEqual(
                len(all_exit_items),
                3,
                f"section '{exit_heading.title}' in {label} must enumerate multiple exit criteria",
            )
            self.assertRegex(
                exit_prose,
                r"(?i)\b(?:m1\s+is\s+not\s+complete|"
                r"m1\s+remains?\s+in[ -]progress|"
                r"exit\s+(?:criteria|obligations)\s+remain\s+(?:open|unchecked))\b",
                f"section '{exit_heading.title}' in {label} must state that M1 remains incomplete",
            )
            self.assertNotRegex(
                exit_prose,
                r"(?i)\bm1\s+(?:is|has\s+been)\s+(?:now\s+)?"
                r"(?:complete|completed|closed|finished)\b",
                f"section '{exit_heading.title}' in {label} must not claim M1 completion",
            )

            stop_section = _find_section(
                document,
                r"^stop criteria$",
                r"^rejection criteria$",
                r"^stop or rejection rules$",
                r"^stop, rejection, and reset criteria$",
            )
            self.assertIsNotNone(
                stop_section,
                f"{label} needs a stop/rejection section",
            )
            assert stop_section is not None
            stop_heading, stop_body = stop_section
            stop_prose = _without_fenced_code(stop_body)
            self.assertGreaterEqual(
                _word_count(stop_body),
                40,
                f"section '{stop_heading.title}' in {label} is not substantive",
            )
            self.assertGreaterEqual(
                _structured_items(stop_body),
                2,
                f"section '{stop_heading.title}' in {label} must enumerate multiple stop/rejection items",
            )
            self.assertRegex(
                stop_prose,
                r"(?i)\b(?:stop|reject|rejection|fail|failure|pause|halt)\b",
                f"section '{stop_heading.title}' in {label} must use explicit stop/reject/fail wording",
            )

        assert_exit_and_stop_criteria_are_valid(foundation, label=FOUNDATION)

        current_exit_section = _find_section(
            foundation,
            r"^exit criteria$",
            r"^launch exit criteria$",
            r"^m1 exit criteria$",
        )
        assert current_exit_section is not None
        self.assertGreaterEqual(
            len(re.findall(r"(?im)^\s*-\s*\[[xX]\]\s+\S.*$", current_exit_section[1])),
            1,
            "the current milestone fixture must exercise partial-progress checkbox semantics",
        )

        all_complete_mutation = re.sub(
            r"(?m)^(\s*-\s*)\[ \](\s+\S.*)$",
            r"\1[x]\2",
            foundation,
        )
        with self.assertRaisesRegex(AssertionError, "multiple unchecked exit criteria"):
            assert_exit_and_stop_criteria_are_valid(
                all_complete_mutation,
                label="mutation falsely marking every exit criterion complete",
            )

        hidden_open_obligations_mutation = re.sub(
            r"(?m)^(\s*-\s*)\[ \](\s+\S.*)$",
            r"\1\2",
            foundation,
        )
        with self.assertRaisesRegex(AssertionError, "multiple unchecked exit criteria"):
            assert_exit_and_stop_criteria_are_valid(
                hidden_open_obligations_mutation,
                label="mutation hiding open obligations as ordinary bullets",
            )

        false_completion_mutation = foundation.replace(
            "M1 is not complete.",
            "M1 is complete.",
            1,
        )
        self.assertNotEqual(foundation, false_completion_mutation)
        with self.assertRaisesRegex(AssertionError, "must state that M1 remains incomplete"):
            assert_exit_and_stop_criteria_are_valid(
                false_completion_mutation,
                label="mutation falsely claiming M1 completion",
            )

        removed_stop_language_mutation = re.sub(
            r"(?is)(## Stop, rejection, and reset criteria\n)(.*?)(?=\n## \S|\Z)",
            "\\1\n"
            "Conditions needing later governance attention:\n\n"
            "- An unresolved subject, study, profile, finding, or artifact digest triggers a documented integrity assessment before additional substantive work proceeds, with the affected identity and scope preserved for review.\n"
            "- Omitted contradictory, null, negative, invalid, or unexecuted outcomes trigger a retention audit that restores visibility without rewriting the underlying record or inventing a favorable disposition.\n"
            "- Work requiring an unsupported method profile returns to separately versioned contract design with its assumptions, risks, and unperformed analyses recorded explicitly.\n",
            foundation,
            count=1,
        )
        mutated_stop_section = _find_section(
            removed_stop_language_mutation,
            r"^stop criteria$",
            r"^rejection criteria$",
            r"^stop or rejection rules$",
            r"^stop, rejection, and reset criteria$",
        )
        assert mutated_stop_section is not None
        self.assertGreaterEqual(_word_count(mutated_stop_section[1]), 40)
        self.assertGreaterEqual(_structured_items(mutated_stop_section[1]), 2)
        self.assertNotRegex(
            _without_fenced_code(mutated_stop_section[1]),
            r"(?i)\b(?:stop|reject|rejection|fail|failure|pause|halt)\b",
        )
        with self.assertRaisesRegex(AssertionError, "must use explicit stop/reject/fail wording"):
            assert_exit_and_stop_criteria_are_valid(
                removed_stop_language_mutation,
                label="mutation without explicit stop/rejection wording",
            )

    def test_04_launch_artifacts_make_no_validation_novelty_or_adoption_claim(self) -> None:
        unsafe_claims = (
            re.compile(
                r"(?i)\b(?:m1|lcmrp|this (?:work|artifact|launch package)|"
                r"(?:the|this|candidate) taxonomy|"
                r"(?:the|this|candidate) (?:formal )?model)\s+"
                r"(?:is|are|has been|constitutes?|establishes?|demonstrates?|proves?)\s+"
                r"(?:scientifically |independently )?"
                r"(?:validated|novel|adopted|replicated|benchmarked|evidence)\b"
            ),
            re.compile(
                r"(?i)\b(?:we|lcmrp)\s+"
                r"(?:demonstrate|prove|confirm|validate|establish)\s+"
                r"(?:the\s+)?(?:taxonomy|model|mechanism|effectiveness|novelty)\b"
            ),
            re.compile(
                r"(?i)\b(?:results?|findings?|evidence)\s+"
                r"(?:demonstrate|prove|confirm|show|establish)\b"
            ),
            re.compile(
                r"(?i)\b(?:m1|lcmrp|this (?:work|artifact|launch package)|"
                r"(?:the|this|candidate) taxonomy|"
                r"(?:the|this|candidate) (?:formal )?model)\s+"
                r"(?:is|are|has been|should be|must be)\s+"
                r"(?:production[- ]ready|ready for (?:product )?"
                r"(?:adoption|integration|production)|adopted)\b"
            ),
        )
        for relative in LAUNCH_PATHS:
            prose = _without_fenced_code(self._doc(relative))
            for pattern in unsafe_claims:
                with self.subTest(document=relative, pattern=pattern.pattern):
                    self.assertIsNone(
                        pattern.search(prose),
                        f"{relative} contains a prohibited positive maturity/evidence claim",
                    )

    def test_05_no_mechanism_evidence_label_is_assigned(self) -> None:
        assignment = re.compile(
            r"(?i)^\s*(?:[-*]\s*)?(?:\*\*)?"
            r"(?:(?:mechanism[_ -]?)?evidence[_ -]?(?:status|state|label)|"
            r"maturity[_ -]?(?:status|state|label)?|status)"
            r"(?:\*\*)?\s*:\s*(?:\*\*)?(.+?)(?:\*\*)?\s*$"
        )
        for relative in LAUNCH_PATHS:
            for line_number, line in enumerate(self._doc(relative).splitlines(), start=1):
                match = assignment.match(_plain_metadata_line(line))
                if not match:
                    continue
                normalized = re.sub(r"[_ -]+", " ", match.group(1).upper())
                assigned = {
                    label
                    for label in MECHANISM_EVIDENCE_LABELS
                    if re.sub(r"[_ -]+", " ", label) in normalized
                }
                self.assertFalse(
                    assigned,
                    f"{relative}:{line_number} assigns mechanism evidence label(s) {sorted(assigned)}",
                )

    def test_06_architectural_independence_is_explicit_and_not_contradicted(self) -> None:
        independence = self._required_section(
            FOUNDATION,
            r"architect(?:ural|ure) independence",
            r"architectural and implementation boundary",
            r"product[- ]independence",
            min_words=45,
        ).lower()
        category_patterns = (
            r"vendor|provider",
            r"storage|database",
            r"model|embedding",
            r"product|application schema|user interface",
            r"cloud|connectivity|offline",
            r"compute|hardware",
        )
        covered = sum(bool(re.search(pattern, independence)) for pattern in category_patterns)
        self.assertGreaterEqual(
            covered,
            4,
            "architectural independence must cover vendor, storage/model, product, and operational assumptions",
        )

        bound_subject = (
            r"(?:lcmrp|m1|this (?:taxonomy|model|program)|"
            r"(?:the|this|candidate) (?:taxonomy|formal model)|"
            r"reference implementations?|memory objects?)"
        )
        binding = r"(?:requires?|must use|shall use|depends? on|standardizes? on|assumes?)"
        technology = (
            r"(?:openai|anthropic|google|aws|azure|pinecone|weaviate|chroma|faiss|"
            r"postgres(?:ql)?|pgvector|redis|qdrant|milvus|vector database|"
            r"language model vendor|embedding model|cloud connectivity|"
            r"application schema|user interface|corpusstudio)"
        )
        positive_binding = re.compile(
            rf"(?i)\b{bound_subject}\b[^.\n]{{0,100}}\b{binding}\b"
            rf"[^.\n]{{0,100}}\b{technology}\b"
        )
        for relative in LAUNCH_PATHS:
            prose = _without_fenced_code(self._doc(relative))
            for match in positive_binding.finditer(prose):
                sentence = match.group(0).lower()
                rejection_markers = (
                    "does not",
                    "must not",
                    "not require",
                    "not assume",
                    "without requiring",
                    "countermodel",
                    "rejected",
                    "prohibited",
                    "violates",
                    "invalid",
                )
                self.assertTrue(
                    any(marker in sentence for marker in rejection_markers),
                    f"{relative} appears to bind the research model to a vendor, storage, or product assumption: {match.group(0)!r}",
                )

    def test_07_corpusstudio_mentions_obey_the_isolated_implications_boundary(self) -> None:
        required_title = "Future CorpusStudio Integration Implications"
        for relative in LAUNCH_PATHS:
            text = self._doc(relative)
            lines = text.splitlines()
            headings = _headings(text)
            allowed_ranges: list[tuple[int, int, str]] = []
            for position, heading in enumerate(headings):
                if heading.title.lower() != required_title.lower():
                    continue
                end = len(lines)
                for later in headings[position + 1 :]:
                    if later.level <= heading.level:
                        end = later.line_index
                        break
                body = "\n".join(lines[heading.line_index + 1 : end])
                allowed_ranges.append((heading.line_index, end, body))

            mentions = [
                index
                for index, line in enumerate(lines)
                if re.search(r"(?i)\bcorpusstudio\b", line)
            ]
            if not mentions:
                continue
            self.assertTrue(
                allowed_ranges,
                f"{relative} mentions CorpusStudio outside the required isolated section",
            )
            for line_index in mentions:
                self.assertTrue(
                    any(start <= line_index < end for start, end, _ in allowed_ranges),
                    f"{relative}:{line_index + 1} has an out-of-boundary CorpusStudio mention",
                )
            for _, _, body in allowed_ranges:
                self.assertIn(
                    "RESEARCH-TO-PRODUCT HYPOTHESIS",
                    body,
                    f"{relative} integration implications lack the required provisional label",
                )

    def test_08_prior_art_contains_a_structural_competing_taxonomy_comparison(self) -> None:
        prior_art = self._doc(PRIOR_ART)
        comparison = _find_section(
            prior_art,
            r"competing taxonom",
            r"taxonomy comparison",
            r"comparison matrix",
            r"taxonomies compared",
        )
        self.assertIsNotNone(
            comparison,
            "prior-art document needs a named competing-taxonomy comparison section",
        )
        assert comparison is not None
        heading, body = comparison
        self.assertGreaterEqual(
            _word_count(body),
            120,
            f"'{heading.title}' is too small to document meaningful comparison",
        )
        compared_rows = _table_data_rows(body)
        child_headings = [
            item
            for item in _headings(body)
            if item.level >= 3 and not re.search(r"references|notes", item.title, re.I)
        ]
        self.assertGreaterEqual(
            max(compared_rows, len(child_headings)),
            3,
            "the prior-art comparison must structurally distinguish at least three competing taxonomies",
        )

    def test_09_taxonomy_defines_types_and_observable_distinctions(self) -> None:
        taxonomy = self._doc(TAXONOMY)
        type_section = _find_section(
            taxonomy,
            r"candidate term register",
            r"core (?:memory )?(?:types|categories)",
            r"functional (?:memory )?(?:types|taxonomy)",
            r"memory (?:types|categories)",
            r"normative taxonomy",
        )
        self.assertIsNotNone(type_section, "taxonomy needs a named memory-type section")
        assert type_section is not None
        heading, type_body = type_section
        self.assertGreaterEqual(
            _word_count(type_body),
            180,
            f"'{heading.title}' does not contain substantive type definitions",
        )
        type_rows = _table_data_rows(type_body)
        type_subheadings = [
            item for item in _headings(type_body) if item.level >= 3
        ]
        self.assertGreaterEqual(
            max(type_rows, len(type_subheadings)),
            5,
            "the taxonomy must structurally define at least five memory types/categories",
        )

        observable = _find_section(
            taxonomy,
            r"observable distinctions?",
            r"operational distinctions?",
            r"discriminating observations?",
            r"classification (?:tests?|criteria)",
        )
        if observable is None:
            observable = _find_section(
                self._doc(PRIOR_ART),
                r"observable distinctions?",
                r"operational distinctions?",
                r"discriminating observations?",
            )
        self.assertIsNotNone(
            observable,
            "launch package needs a named observable-distinction section",
        )
        assert observable is not None
        _, observable_body = observable
        self.assertGreaterEqual(_word_count(observable_body), 80)
        self.assertGreaterEqual(
            _structured_items(observable_body),
            4,
            "observable distinctions must be expressed as multiple checkable criteria",
        )

    def test_10_edge_cases_and_unresolved_obligations_are_explicit(self) -> None:
        edge_case_section: tuple[Heading, str] | None = None
        for relative in (TAXONOMY, FORMAL_MODEL, PRIOR_ART):
            edge_case_section = _find_section(
                self._doc(relative), r"edge cases?", r"boundary cases?", r"ambiguous cases?"
            )
            if edge_case_section:
                break
        self.assertIsNotNone(edge_case_section, "launch package needs an edge-case section")
        assert edge_case_section is not None
        _, edge_body = edge_case_section
        self.assertGreaterEqual(_word_count(edge_body), 60)
        self.assertGreaterEqual(
            _structured_items(edge_body),
            3,
            "edge cases must enumerate at least three distinct boundaries",
        )

        obligation_section: tuple[Heading, str] | None = None
        for relative in (FOUNDATION, TAXONOMY, FORMAL_MODEL, PRIOR_ART):
            obligation_section = _find_section(
                self._doc(relative),
                r"unresolved (?:obligations?|questions?)",
                r"open (?:validation )?obligations?",
                r"open questions?",
                r"proof obligations?",
            )
            if obligation_section:
                break
        self.assertIsNotNone(
            obligation_section,
            "M1 launch package needs an explicit unresolved-obligations section",
        )
        assert obligation_section is not None
        _, obligations = obligation_section
        self.assertGreaterEqual(
            _word_count(obligations),
            60,
            "unresolved-obligations section is not substantive",
        )
        self.assertGreaterEqual(
            _structured_items(obligations),
            4,
            "M1 launch must enumerate unresolved obligations instead of implying completion",
        )

    def test_11_formal_model_has_typed_objects(self) -> None:
        typed = self._required_section(
            FORMAL_MODEL,
            r"typed objects?",
            r"typed domains?",
            r"object types?",
            r"type system",
            r"core types?",
            min_words=100,
        )
        code_free = _without_fenced_code(typed)
        prose_declaration_count = len(
            re.findall(
                r"(?im)^\s*(?:[-*]\s+)?(?:\*\*)?[A-Z][A-Za-z0-9_ ]+"
                r"(?:\*\*)?\s*(?::=|:|[—–-])\s+\S",
                code_free,
            )
        )
        formal_declaration_count = len(
            re.findall(
                r"(?im)^\s*(?:type|record|class)\s+[A-Z][A-Za-z0-9_]*\b|"
                r"^\s*[A-Z][A-Za-z0-9_]*\s*:=",
                typed,
            )
        )
        self.assertGreaterEqual(
            max(_table_data_rows(typed), prose_declaration_count, formal_declaration_count),
            3,
            "formal model must structurally define multiple typed objects",
        )

    def test_12_formal_model_has_lifecycle_time_actors_and_operations(self) -> None:
        lifecycle = self._required_section(FORMAL_MODEL, r"lifecycle", min_words=45)
        self.assertGreaterEqual(
            max(
                _structured_items(lifecycle),
                len(_headings(lifecycle)),
                len(re.findall(r"(?:-->|→)", lifecycle)),
            ),
            4,
            "lifecycle must expose multiple states or transitions",
        )

        time_model = self._required_section(
            FORMAL_MODEL, r"time model", r"temporal model", r"temporal semantics", min_words=60
        )
        temporal_concepts = {
            match.group(0).lower().replace("_", " ")
            for match in re.finditer(
                r"(?i)\b(?:event[_ ]time|observation[_ ]time|recorded[_ ]at|"
                r"occurred[_ ]at|valid[_ ]from|valid[_ ]to|system[_ ]time|"
                r"transaction[_ ]time|temporal order|interval|instant|clock)\b",
                time_model,
            )
        }
        self.assertGreaterEqual(
            len(temporal_concepts),
            2,
            "time model must distinguish at least two temporal concepts",
        )

        actors = self._required_section(
            FORMAL_MODEL, r"actors?(?: and authority)?", r"authority model", min_words=60
        )
        self.assertGreaterEqual(
            max(_structured_items(actors), len(_headings(actors))),
            3,
            "actor/authority model must distinguish multiple actors or roles",
        )

        operations = self._required_section(
            FORMAL_MODEL, r"operations?", r"operation algebra", min_words=100
        )
        self.assertGreaterEqual(
            _structured_items(operations),
            5,
            "formal model must define multiple memory lifecycle operations",
        )

    def test_13_formal_model_states_invariants_countermodels_and_non_entailments(self) -> None:
        invariants = self._required_section(FORMAL_MODEL, r"invariants?", min_words=70)
        self.assertGreaterEqual(
            max(_structured_items(invariants), len(_headings(invariants))),
            3,
            "formal model needs at least three explicit invariants",
        )

        countermodels = self._required_section(
            FORMAL_MODEL, r"countermodels?", r"invalid models?", min_words=60
        )
        self.assertGreaterEqual(
            max(_structured_items(countermodels), len(_headings(countermodels))),
            2,
            "formal model needs multiple countermodels that would violate its definitions",
        )

        non_entailments = self._required_section(
            FORMAL_MODEL, r"non[- ]entailments?", r"does not entail", min_words=70
        )
        self.assertGreaterEqual(
            _structured_items(non_entailments),
            3,
            "formal model must enumerate what its definitions do not establish",
        )

    def test_14_authority_provenance_confidence_and_deletion_have_semantics(self) -> None:
        authority = self._required_section(
            FORMAL_MODEL, r"actors?(?: and authority)?", r"authority model", min_words=60
        ).lower()
        self.assertRegex(
            authority,
            r"\b(?:authoriz|permission|may\b|must\b|authority|control)\w*",
            "actor list must define authority rather than only name roles",
        )

        provenance = self._required_section(
            FORMAL_MODEL, r"provenance(?: model| semantics)?", min_words=70
        ).lower()
        provenance_dimensions = sum(
            term in provenance
            for term in (
                "source",
                "actor",
                "observation",
                "derivation",
                "origin",
                "time",
                "integrity",
                "unknown",
            )
        )
        self.assertGreaterEqual(
            provenance_dimensions,
            4,
            "provenance semantics must cover source/origin, derivation or observation, time, and uncertainty/integrity",
        )

        confidence = self._required_section(
            FORMAL_MODEL, r"confidence(?: and uncertainty)?", r"uncertainty", min_words=70
        ).lower()
        self.assertRegex(
            confidence,
            r"(?s)(?:confidence.{0,100}\bnot\b.{0,100}(?:truth|correct|accuracy|authority)|"
            r"(?:truth|correct|accuracy|authority).{0,100}\bnot\b.{0,100}confidence|"
            r"no (?:calibration|probabilistic interpretation|accuracy|truth|correctness|authority)"
            r".{0,100}follows from (?:this|a|the) (?:confidence |assessment |interval|value))",
            "confidence semantics must state that confidence does not entail truth/correctness/authority",
        )

        deletion = self._required_section(
            FORMAL_MODEL, r"deletion(?: semantics)?", r"deletion and erasure", min_words=90
        ).lower()
        deletion_dimensions = sum(
            bool(re.search(pattern, deletion))
            for pattern in (
                r"tombstone|unavailable|retriev",
                r"purge|physical|erasure|destroy",
                r"deriv|cop(?:y|ies)|propagat",
                r"verif|audit|evidence",
                r"retention|authoriz|policy",
            )
        )
        self.assertGreaterEqual(
            deletion_dimensions,
            3,
            "deletion semantics must address retrieval state, physical/derived data, and authorization or verification",
        )

    def test_15_launch_declares_no_registry_or_finding_effect(self) -> None:
        boundary = self._required_section(
            FOUNDATION,
            r"evidence and registry boundary",
            r"evidence and reporting boundary",
            r"registry (?:effect|boundary)",
            r"research evidence boundary",
            min_words=35,
        )
        self.assertRegex(
            boundary,
            r"(?i)\b(?:registr(?:y|ies).{0,80}(?:remain|stay|are) empty|"
            r"no (?:production )?registr(?:y|ies) (?:is|are|was|were) (?:changed|populated)|"
            r"no (?:registry )?(?:records?|entries) (?:are|were|have been) (?:created|added|populated))\b",
            "M1 launch must explicitly state that it creates no registry entries",
        )
        self.assertRegex(
            boundary,
            r"(?i)\b(?:no (?:research )?(?:findings?|results?|evidence) (?:are|were|have been) (?:claimed|created|recorded|established)|"
            r"(?:make|assert|report|record)s? no (?:empirical |research |scientific )?(?:findings?|results?)|"
            r"does not (?:constitute|establish) (?:a )?(?:research )?(?:finding|evidence))\b",
            "M1 launch must explicitly disclaim fabricated findings/evidence",
        )

        record_assignment = re.compile(
            r"(?im)^\s*(?:[-*]\s*)?(?:finding|evidence|experiment|study)[_-]?id\s*"
            r"[:=]\s*[`\"']?[a-z0-9]"
        )
        result_assignment = re.compile(
            r"(?im)^\s*(?:[-*]\s*)?(?:result|finding)s?\s*:\s*"
            r"(?:passed|confirmed|supported|validated|accepted)\b"
        )
        for relative in LAUNCH_PATHS:
            prose = _without_fenced_code(self._doc(relative))
            self.assertIsNone(
                record_assignment.search(prose),
                f"{relative} appears to embed a populated evidence/study/finding record",
            )
            self.assertIsNone(
                result_assignment.search(prose),
                f"{relative} appears to assert an empirical result during launch",
            )

    def test_16_foundation_links_the_package_and_all_relative_links_resolve(self) -> None:
        markdown_link = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
        foundation_targets: set[Path] = set()

        for relative in LAUNCH_PATHS:
            source_path = self.paths[relative]
            text = self._doc(relative)
            for raw_target in markdown_link.findall(text):
                raw_target = raw_target.strip()
                if raw_target.startswith("<") and ">" in raw_target:
                    raw_target = raw_target[1 : raw_target.index(">")]
                else:
                    raw_target = raw_target.split(maxsplit=1)[0]
                parsed = urlsplit(raw_target)
                if parsed.scheme or parsed.netloc or raw_target.startswith(("mailto:", "data:")):
                    continue

                decoded_path = unquote(parsed.path)
                target_path = source_path if not decoded_path else source_path.parent / decoded_path
                resolved = target_path.resolve()
                try:
                    resolved.relative_to(ROOT.resolve())
                except ValueError:
                    self.fail(f"{relative} has a relative link escaping the repository: {raw_target}")
                self.assertTrue(
                    resolved.exists(),
                    f"{relative} has broken relative link {raw_target!r} -> {resolved}",
                )

                if relative == FOUNDATION:
                    foundation_targets.add(resolved)

                if parsed.fragment and resolved in {path.resolve() for path in self.paths.values()}:
                    target_relative = next(
                        key for key, path in self.paths.items() if path.resolve() == resolved
                    )
                    slugs = {_github_slug(item.title) for item in _headings(self._doc(target_relative))}
                    self.assertIn(
                        unquote(parsed.fragment).lower(),
                        slugs,
                        f"{relative} links to a missing launch-package anchor: {raw_target}",
                    )

        expected_companions = {
            self.paths[relative].resolve() for relative in (PRIOR_ART, TAXONOMY, FORMAL_MODEL)
        }
        self.assertTrue(
            expected_companions.issubset(foundation_targets),
            "M1 foundation must link all three companion research artifacts",
        )

    def test_17_versioned_register_and_declared_ids_are_unique(self) -> None:
        """Bind identity checks to structural declarations, never prose mentions."""

        taxonomy = self._doc(TAXONOMY)
        register = _find_section(taxonomy, r"candidate term register")
        self.assertIsNotNone(register, "taxonomy needs a candidate term register")
        assert register is not None
        _, register_body = register

        # Only tables whose first header is "Candidate ID" are register tables.
        # This avoids counting examples, cross-references, or prose mentions as
        # declarations. Every data row in such a table must carry a valid ID.
        lines = register_body.splitlines()
        register_ids: list[str] = []
        register_table_count = 0
        index = 0
        while index < len(lines):
            line = lines[index]
            if "|" not in line:
                index += 1
                continue
            headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if not headers or headers[0].lower() != "candidate id":
                index += 1
                continue
            self.assertLess(index + 1, len(lines), "register table lacks a separator row")
            separators = [
                cell.strip()
                for cell in lines[index + 1].strip().strip("|").split("|")
            ]
            self.assertEqual(len(headers), len(separators), "register table is ragged")
            self.assertTrue(
                all(re.fullmatch(r":?-{3,}:?", cell) for cell in separators),
                "Candidate ID header must begin a Markdown table",
            )

            register_table_count += 1
            index += 2
            while index < len(lines) and "|" in lines[index]:
                cells = [
                    cell.strip() for cell in lines[index].strip().strip("|").split("|")
                ]
                self.assertEqual(
                    len(headers),
                    len(cells),
                    f"candidate-register row is ragged: {lines[index]!r}",
                )
                candidate_id = re.sub(r"[*_`]", "", cells[0]).strip()
                self.assertRegex(
                    candidate_id,
                    r"^LCMRP-TAX-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{3}@0\.1$",
                    f"candidate-register row has an unversioned or malformed ID: {candidate_id!r}",
                )
                self.assertTrue(
                    all(cell.strip() for cell in cells[1:]),
                    f"candidate-register row {candidate_id!r} has an empty substantive field",
                )
                register_ids.append(candidate_id)
                index += 1

        self.assertGreaterEqual(
            register_table_count,
            2,
            "candidate term register must span multiple structurally declared tables",
        )
        self.assertGreaterEqual(
            len(register_ids),
            5,
            "candidate term register is not substantive",
        )
        self.assertEqual(
            len(register_ids),
            len(set(register_ids)),
            "candidate term register contains duplicate exact IDs",
        )

        objectives = _find_section(self._doc(FOUNDATION), r"falsifiable launch objectives")
        self.assertIsNotNone(objectives, "M1 foundation needs falsifiable launch objectives")
        assert objectives is not None
        objective_ids = [
            match.group(1)
            for heading in _headings(objectives[1])
            if (match := re.match(r"^(M1-O\d+)\b", heading.title))
        ]
        self.assertGreaterEqual(len(objective_ids), 2, "M1 objective set is not substantive")
        self.assertEqual(
            len(objective_ids),
            len(set(objective_ids)),
            "M1 objective headings contain duplicate IDs",
        )

        formal = self._doc(FORMAL_MODEL)
        for section_pattern, id_pattern, label in (
            (r"candidate invariants?", r"^(FMO-INV-\d{2,})\b", "formal invariant"),
            (r"candidate countermodels?", r"^(CM-\d{2,})\b", "countermodel"),
        ):
            declared = _find_section(formal, section_pattern)
            self.assertIsNotNone(declared, f"formal model needs a {label} section")
            assert declared is not None
            declared_ids = [
                match.group(1)
                for heading in _headings(declared[1])
                if (match := re.match(id_pattern, heading.title))
            ]
            self.assertGreaterEqual(
                len(declared_ids),
                2,
                f"{label} declaration set is not substantive",
            )
            self.assertEqual(
                len(declared_ids),
                len(set(declared_ids)),
                f"{label} headings contain duplicate IDs",
            )


if __name__ == "__main__":
    unittest.main()
