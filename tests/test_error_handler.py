import pytest

from sshr.assistant.error.error_handler import Error, ErrorValueOutOfRange


class TestErrorInit:
    def test_creates_with_valid_code(self):
        err = Error("ERR001")
        assert err.error == "ERR001"
        assert err.text is not None

    def test_creates_with_last_code(self):
        err = Error("ERR016")
        assert err.error == "ERR016"

    def test_raises_on_out_of_range_code(self):
        with pytest.raises(ErrorValueOutOfRange):
            Error("ERR999")

    def test_raises_on_malformed_code(self):
        with pytest.raises(ErrorValueOutOfRange):
            Error("invalid")


class TestErrorText:
    def test_includes_message(self, capsys):
        Error("ERR001").print_er()
        out = capsys.readouterr().out
        assert "[ERR001]" in out

    def test_excludes_help_key(self):
        err = Error("ERR001")
        assert "description" not in err.text
        assert "solution" not in err.text

    def test_includes_tip(self, capsys):
        Error("ERR001").print_er()
        out = capsys.readouterr().out
        assert "tip" not in out
        assert out != ""

    def test_appends_footer(self):
        err = Error("ERR001")
        assert "--help" in err.text
        assert "ERR001" in err.text


class TestErrorFormat:
    def test_format_interpolates_single_placeholder(self):
        err = Error("ERR011")
        err.format(type=int)
        assert "int" in err.text

    def test_format_interpolates_command_placeholder(self):
        err = Error("ERR014")
        err.format(command="register")
        assert "register" in err.text

    def test_format_returns_self_for_chaining(self, capsys):
        result = Error("ERR011").format(type=int).print_er()
        assert result is None
        out = capsys.readouterr().out
        assert "int" in out


class TestErrorPrint:
    def test_print_output(self, capsys):
        Error("ERR013").print_er()
        out = capsys.readouterr().out
        assert "ERR013" in out
        assert "No arguments provided" in out
        assert "--help ERR013" in out
