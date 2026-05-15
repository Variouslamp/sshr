import pytest

from sshr.core.internal.validation import validar_flag, validator
from sshr.core.internal.flags import COMANDOS


SAMPLE_DICT = {
    "register": {"flags": ["-r", "--register"]},
    "list": {"flags": ["-l", "-ll", "--list"]},
    "help": {"flags": ["-h", "--help"]},
    "build": {"flags": ["build"]},
    "edit": {"flags": ["-e", "--edit"]},
}


class TestValidarFlag:
    def test_returns_command_for_short_flag(self):
        assert validar_flag("-r", SAMPLE_DICT) == "register"

    def test_returns_command_for_long_flag(self):
        assert validar_flag("--register", SAMPLE_DICT) == "register"

    def test_returns_command_for_list_short(self):
        assert validar_flag("-l", SAMPLE_DICT) == "list"

    def test_returns_command_for_list_double(self):
        assert validar_flag("-ll", SAMPLE_DICT) == "list"

    def test_returns_command_for_list_long(self):
        assert validar_flag("--list", SAMPLE_DICT) == "list"

    def test_returns_command_for_help_short(self):
        assert validar_flag("-h", SAMPLE_DICT) == "help"

    def test_returns_command_for_help_long(self):
        assert validar_flag("--help", SAMPLE_DICT) == "help"

    def test_returns_command_for_build(self):
        assert validar_flag("build", SAMPLE_DICT) == "build"

    def test_returns_false_for_unknown_flag(self):
        assert validar_flag("--invalid", SAMPLE_DICT) is False

    def test_returns_false_for_empty_string(self):
        assert validar_flag("", SAMPLE_DICT) is False

    def test_works_with_real_comandos(self):
        assert validar_flag("--register", COMANDOS) == "register"
        assert validar_flag("-d", COMANDOS) == "delete"
        assert validar_flag("--edit", COMANDOS) == "edit"


class TestValidator:
    def test_valid_int_input(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "42")
        assert validator(int, "Enter: ") == 42

    def test_valid_str_input(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "hello")
        assert validator(str, "Enter: ") == "hello"

    def test_retries_on_invalid_input(self, monkeypatch):
        inputs = iter(["abc", "10"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        assert validator(int, "Enter: ") == 10

    def test_empty_text_prompt(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "data")
        assert validator(str) == "data"
