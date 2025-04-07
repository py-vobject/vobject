import subprocess
from typing import List


class Cli:
    ics_diff = "ics_diff"
    change_tz = "change_tz"


def run_cli_tool(toolname: str, args: List[str]):
    return subprocess.run([toolname] + args, capture_output=True, text=True, check=False)


def test_change_tz():
    result = run_cli_tool(Cli.change_tz, ["--version"])
    assert result.returncode == 0

    result = run_cli_tool(Cli.change_tz, [])
    assert result.returncode == 2
    assert "one of the arguments -l/--list ics_file is required" in result.stderr


def test_ics_diff():
    result = run_cli_tool(Cli.ics_diff, ["--version"])
    assert result.returncode == 0

    result = run_cli_tool(Cli.ics_diff, [])
    assert result.returncode == 2
    assert "required: ics_file1, ics_file2" in result.stderr
