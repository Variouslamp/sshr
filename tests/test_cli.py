import os
import subprocess
import sys
from pathlib import Path

import pytest

from sshr.core.cli import validar_cantidad, flags_dict
from sshr.core.internal.flags import COMANDOS


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


# ── Subprocess tests (integration via CLI entry point) ──────────────────────


def run_cli(*args):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC)
    return subprocess.run(
        [sys.executable, "-m", "sshr.core.cli", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


class TestCliIntegration:
    def test_cli_without_args_shows_error(self):
        result = run_cli()
        assert result.returncode == 0
        assert "ERR013" in result.stdout

    def test_cli_with_invalid_flag(self):
        result = run_cli("--invalid")
        assert result.returncode == 0
        assert "ERR012" in result.stdout

    def test_cli_with_wrong_arg_count_for_register(self):
        result = run_cli("-r")
        assert result.returncode == 1
        assert "ERR014" in result.stdout

    def test_cli_with_help_no_args(self):
        result = run_cli("-h")
        assert result.returncode == 0
        assert result.stdout.strip() != ""

    def test_cli_with_help_and_command(self):
        result = run_cli("-h", "register")
        assert result.returncode == 0
        assert "register" in result.stdout.lower()

    def test_cli_with_help_and_unknown_command(self):
        result = run_cli("-h", "nonexistent")
        assert result.returncode == 0
        assert "ERR016" in result.stdout


# ── Unit tests for validar_cantidad ─────────────────────────────────────────


class MockFlags:
    """Minimal mock that mimics the shape used by validar_cantidad."""
    fixed_cmd = {"input_args": 2}
    range_cmd = {"min_input_args": 1, "max_input_args": 2}


class TestValidarCantidad:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.original = flags_dict.copy()

    def test_exact_match_fixed(self, monkeypatch):
        monkeypatch.setitem(COMANDOS, "test_fixed", MockFlags.fixed_cmd)
        monkeypatch.setitem(COMANDOS, "test_range", MockFlags.range_cmd)

    def test_fixed_correct_arg_count(self, monkeypatch):
        monkeypatch.setitem(COMANDOS, "cmd", {"input_args": 2})
        assert validar_cantidad("cmd", 2) is True

    def test_fixed_wrong_arg_count_exits(self, monkeypatch):
        monkeypatch.setitem(COMANDOS, "cmd", {"input_args": 2})
        with pytest.raises(SystemExit):
            validar_cantidad("cmd", 1)

    def test_range_correct_min(self, monkeypatch):
        monkeypatch.setitem(COMANDOS, "cmd", {"min_input_args": 1, "max_input_args": 2})
        assert validar_cantidad("cmd", 1) is True

    def test_range_correct_max(self, monkeypatch):
        monkeypatch.setitem(COMANDOS, "cmd", {"min_input_args": 1, "max_input_args": 2})
        assert validar_cantidad("cmd", 2) is True

    def test_range_below_min_exits(self, monkeypatch):
        monkeypatch.setitem(COMANDOS, "cmd", {"min_input_args": 1, "max_input_args": 2})
        with pytest.raises(SystemExit):
            validar_cantidad("cmd", 0)

    def test_range_above_max_exits(self, monkeypatch):
        monkeypatch.setitem(COMANDOS, "cmd", {"min_input_args": 1, "max_input_args": 2})
        with pytest.raises(SystemExit):
            validar_cantidad("cmd", 3)

    def test_register_requires_2_args(self):
        assert validar_cantidad("register", 2) is True

    def test_register_wrong_args_exits(self):
        with pytest.raises(SystemExit):
            validar_cantidad("register", 1)

    def test_help_accepts_1_arg(self):
        assert validar_cantidad("help", 1) is True

    def test_help_accepts_2_args(self):
        assert validar_cantidad("help", 2) is True

    def test_edit_requires_1_arg(self):
        assert validar_cantidad("edit", 1) is True

    def test_list_requires_1_arg(self):
        assert validar_cantidad("list", 1) is True

    def test_delete_requires_1_arg(self):
        assert validar_cantidad("delete", 1) is True


class TestFlagsDict:
    def test_flags_dict_is_comandos(self):
        assert flags_dict is COMANDOS
