import pytest

from sshr.core.internal.flags import COMANDOS


REQUIRED_COMMANDS = ["register", "edit", "list", "delete", "build", "help"]

REQUIRED_KEYS_FIXED = {"flags", "used_args", "input_args", "need_args"}
REQUIRED_KEYS_RANGE = {"flags", "used_args", "min_input_args", "max_input_args", "need_args"}


class TestComandosStructure:
    def test_all_commands_present(self):
        assert set(COMANDOS.keys()) == set(REQUIRED_COMMANDS)

    def test_each_command_has_required_keys(self):
        for cmd in REQUIRED_COMMANDS:
            keys = set(COMANDOS[cmd].keys())
            if cmd == "help":
                assert REQUIRED_KEYS_RANGE.issubset(keys), f"{cmd} missing keys"
            else:
                assert REQUIRED_KEYS_FIXED.issubset(keys), f"{cmd} missing keys"

    def test_flags_are_non_empty_lists(self):
        for cmd in REQUIRED_COMMANDS:
            flags = COMANDOS[cmd]["flags"]
            assert isinstance(flags, list), f"{cmd}.flags not a list"
            assert len(flags) > 0, f"{cmd}.flags is empty"

    def test_need_args_is_list(self):
        for cmd in REQUIRED_COMMANDS:
            assert isinstance(COMANDOS[cmd]["need_args"], list)

    def test_used_args_are_non_negative_ints(self):
        for cmd in REQUIRED_COMMANDS:
            assert isinstance(COMANDOS[cmd]["used_args"], int)
            assert COMANDOS[cmd]["used_args"] >= 0


class TestRegisterFlags:
    def test_flags(self):
        assert COMANDOS["register"]["flags"] == ["-r", "--register"]

    def test_used_args(self):
        assert COMANDOS["register"]["used_args"] == 2

    def test_input_args(self):
        assert COMANDOS["register"]["input_args"] == 2

    def test_need_args(self):
        assert COMANDOS["register"]["need_args"] == ["direccion_conexion", "directorio_ssh"]


class TestEditFlags:
    def test_flags(self):
        assert COMANDOS["edit"]["flags"] == ["-e", "--edit"]

    def test_input_args(self):
        assert COMANDOS["edit"]["input_args"] == 1

    def test_need_args(self):
        assert COMANDOS["edit"]["need_args"] == []


class TestListFlags:
    def test_flags(self):
        assert COMANDOS["list"]["flags"] == ["-l", "-ll", "--list"]

    def test_input_args(self):
        assert COMANDOS["list"]["input_args"] == 1

    def test_need_args(self):
        assert COMANDOS["list"]["need_args"] == ["directorio_ssh", "flag"]


class TestDeleteFlags:
    def test_flags(self):
        assert COMANDOS["delete"]["flags"] == ["-d", "--delete"]

    def test_input_args(self):
        assert COMANDOS["delete"]["input_args"] == 1

    def test_need_args(self):
        assert COMANDOS["delete"]["need_args"] == ["directorio_ssh"]


class TestBuildFlags:
    def test_flags(self):
        assert COMANDOS["build"]["flags"] == ["build"]

    def test_input_args(self):
        assert COMANDOS["build"]["input_args"] == 1

    def test_need_args(self):
        assert COMANDOS["build"]["need_args"] == []


class TestHelpFlags:
    def test_flags(self):
        assert COMANDOS["help"]["flags"] == ["-h", "--help"]

    def test_has_range_args(self):
        assert "min_input_args" in COMANDOS["help"]
        assert "max_input_args" in COMANDOS["help"]
        assert "input_args" not in COMANDOS["help"]

    def test_min_input_args(self):
        assert COMANDOS["help"]["min_input_args"] == 1

    def test_max_input_args(self):
        assert COMANDOS["help"]["max_input_args"] == 2

    def test_need_args(self):
        assert COMANDOS["help"]["need_args"] == ["help_arg"]
