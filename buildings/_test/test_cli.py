"""Fast tests of the command line interface (no browser is opened)"""

import pytest

import buildings
from buildings import cli

def test_open(monkeypatch,capsys):
    """`buildings` opens the notebook URL and returns 0"""
    opened = []
    monkeypatch.setattr(cli.web,"open",lambda url: opened.append(url) or True)
    assert cli.main([]) == cli.E_OK
    assert opened == [cli.NOTEBOOK_URL]
    assert capsys.readouterr().out.endswith("ok\n")

def test_open_fails(monkeypatch,capsys):
    """When no browser opens, print a one-line error and return nonzero"""
    monkeypatch.setattr(cli.web,"open",lambda url: False)
    assert cli.main(["open"]) == cli.E_FAILED
    assert capsys.readouterr().err.startswith("ERROR [buildings]:")

def test_version(capsys):
    """`--version` prints the package version"""
    with pytest.raises(SystemExit) as code:
        cli.main(["--version"])
    assert code.value.code == 0
    assert buildings.__version__ in capsys.readouterr().out

def test_bad_command():
    """Unknown commands are rejected by argparse"""
    with pytest.raises(SystemExit) as code:
        cli.main(["nosuchcommand"])
    assert code.value.code != 0
