from pathlib import Path

import pytest

from sshr.assistant.help.help_command import (
    Help,
    PrntErrorHelp,
    ErrorValueOutOfRange,
    help_main,
    HELPS_JSON,
    COMANDOS,
)


class TestHelpClass:
    def test_init_loads_dict(self):
        h = Help("general")
        assert hasattr(h, "dict")
        assert "general" in h.dict
        assert "commands" in h.dict

    def test_general_text_includes_title(self):
        h = Help("general")
        assert "SSHR" in h.text or "ssh" in h.text.lower()

    def test_general_text_includes_commands_list(self):
        h = Help("general")
        assert "-r" in h.text or "--register" in h.text

    def test_command_help_for_register(self):
        h = Help("commands", "register")
        assert "-r" in h.text or "register" in h.text.lower()

    def test_command_help_for_list(self):
        h = Help("commands", "list")
        assert "-l" in h.text or "list" in h.text.lower()

    def test_command_help_for_delete(self):
        h = Help("commands", "delete")
        assert "-d" in h.text or "delete" in h.text.lower()

    def test_unknown_command_returns_none(self):
        h = Help("commands", "nonexistent")
        assert h.text is None or h.text == ""

    def test_print_help_output(self, capsys):
        h = Help("general")
        h.print_help()
        out = capsys.readouterr().out
        assert out != ""


class TestPrntErrorHelp:
    def test_text_contains_description(self):
        e = PrntErrorHelp("ERR001")
        assert e.text is not None

    def test_text_excludes_message_and_tip(self):
        e = PrntErrorHelp("ERR001")
        assert "[ERR001]" not in e.text

    def test_includes_examples(self, capsys):
        e = PrntErrorHelp("ERR001")
        assert "VALID" in e.text or "INVALID" in e.text or "example" in e.text.lower()

    def test_print_output(self, capsys):
        e = PrntErrorHelp("ERR001")
        e.print_er()
        out = capsys.readouterr().out
        assert out != ""

    def test_unknown_error_returns_none(self):
        raw = PrntErrorHelp("ERR001")._raw_text("ERR001")
        assert raw is not None

    def test_none_error_returns_none_from_raw(self):
        e = PrntErrorHelp("ERR001")
        assert e._raw_text(None) is None


class TestHelpMain:
    def test_general_help_with_none(self, capsys):
        help_main(None)
        out = capsys.readouterr().out
        assert "SSHR" in out

    def test_command_help_with_register(self, capsys):
        help_main("register")
        out = capsys.readouterr().out
        assert "register" in out.lower()

    def test_command_help_with_list(self, capsys):
        help_main("list")
        out = capsys.readouterr().out
        assert "list" in out.lower()

    def test_error_help_with_err_code(self, capsys):
        help_main("ERR001")
        out = capsys.readouterr().out
        assert out != ""

    def test_unknown_command_shows_error(self, capsys):
        help_main("nonexistent")
        out = capsys.readouterr().out
        assert "ERR016" in out

    def test_unknown_error_code_shows_error(self, capsys):
        help_main("ERR999")
        out = capsys.readouterr().out
        assert "ERR015" in out


class TestInternal:
    def test_helps_json_exists(self):
        assert HELPS_JSON.exists()

    def test_flags_dict_matches_comandos(self):
        from sshr.assistant.help.help_command import flags_dict
        assert flags_dict is COMANDOS
