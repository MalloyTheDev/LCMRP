import os
import sys

# make the `fmo` package importable when running `python -m pytest impl/tests`
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
