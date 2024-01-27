"""Tests for venomx."""
from pathlib import Path

import pytest

from venomx.tools.file_io import save_index

THIS = Path(__file__).parent
INPUT_DIR = THIS / "input"
OUTPUT_DIR = THIS / "output"
TEMP_TEST_YAML = OUTPUT_DIR / "temp_test.vx.yaml"
TEMP_COMBINED_YAML = INPUT_DIR / "example.combined.yaml"


