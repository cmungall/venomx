import pytest

from tests import TEMP_TEST_YAML, OUTPUT_DIR, TEMP_COMBINED_YAML
from venomx.tools.cli import main


def test_help(runner):
    """
    Tests help message

    :param runner:
    :return:
    """
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "validate" in result.output



@pytest.mark.parametrize("command,options,arguments,passes,outpath,expected", [
    ("validate", ["--help"], [], True, None, "validate"),
    ("validate", [str(TEMP_TEST_YAML)], [], True, None, ""),
    ("validate", [str(TEMP_COMBINED_YAML)], ["-f", "yaml"], True, None, ""),
    ("convert", [str(TEMP_TEST_YAML)], ["-o", str(OUTPUT_DIR / "tmp.yaml")], True, None, ""),
    ("convert", [str(TEMP_TEST_YAML)], ["-f", "parquet", "-o", str(OUTPUT_DIR / "tmp.yaml")], True, None, ""),
    ("convert", [str(TEMP_TEST_YAML)], ["-t", "yaml", "-o", str(OUTPUT_DIR / "all_in_one.yaml")], True, None, ""),
    ("convert", [str(TEMP_COMBINED_YAML)], ["-f", "yaml", "-o", str(OUTPUT_DIR / "all_in_one.yaml")], True, None, ""),
])
def test_all(create_test_index_files, runner, command, options, arguments, passes, outpath, expected):
    """
    Tests multiple commands

    :param runner:
    :return:
    """
    if outpath is not None:
        outpath.parent.mkdir(exist_ok=True, parents=True)
    result = runner.invoke(main, [command] + options + arguments)
    if result.exit_code != 0:
        print(f"OUTPUT: {result.output}")
    if not passes:
        assert result.exit_code != 0
        return
    assert result.exit_code == 0
    if outpath is None:
        output_text = result.output
    else:
        with open(outpath) as stream:
            output_text = stream.read()
    assert expected in output_text