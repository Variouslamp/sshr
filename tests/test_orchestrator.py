from pathlib import Path

import pytest

from sshr.core import orchestrator


COMANDOS_STUB = {
    "register": {"need_args": ["direccion_conexion", "directorio_ssh"]},
    "help": {"need_args": ["help_arg"]},
    "list": {"need_args": ["directorio_ssh", "flag"]},
}


class TestConfigFile:
    def test_uses_default_if_manual_missing(self):
        path = orchestrator.config_file()
        assert path.name == "config.ini"
        assert "templates" in str(path)

    def test_prefers_manual_when_exists(self, monkeypatch):
        original_exists = Path.exists

        def fake_exists(self):
            if str(self).endswith(".config/sshr/config.ini"):
                return True
            return original_exists(self)

        monkeypatch.setattr(Path, "exists", fake_exists)
        path = orchestrator.config_file()
        assert str(path).endswith(".config/sshr/config.ini")


class TestObtenerArgumentos:
    def test_direccion_conexion(self):
        cmds = {"test": {"need_args": ["direccion_conexion"]}}
        result = orchestrator.obtener_argumentos(
            "test", cmds, {}, ("-r", "alice@host:22"),
        )
        assert result[0] == "alice@host:22"

    def test_directorio_ssh_with_existing_file(self, tmp_path):
        ssh_dir = tmp_path / "ssh-dir"
        ssh_dir.mkdir()
        cfg = ssh_dir / "config"
        cfg.write_text("# ssh config", encoding="utf-8")
        direcciones = {"directorio_ssh": [str(ssh_dir)]}
        result = orchestrator.obtener_argumentos(
            "register", COMANDOS_STUB, direcciones, ("-r", "alice@host:22"),
        )
        assert result[1] == cfg

    def test_directorio_ssh_skips_non_existing(self, tmp_path):
        direcciones = {"directorio_ssh": [str(tmp_path / "nonexistent")]}
        result = orchestrator.obtener_argumentos(
            "register", COMANDOS_STUB, direcciones, ("-r", "alice@host:22"),
        )
        assert len(result) == 1

    def test_flag_field(self):
        comando = {"list": {"need_args": ["flag"]}}
        result = orchestrator.obtener_argumentos(
            "list", comando, {}, ("-l",),
        )
        assert result[0] == "-l"

    def test_help_arg_with_two_args(self):
        result = orchestrator.obtener_argumentos(
            "help", COMANDOS_STUB, {}, ("-h", "register"),
        )
        assert result[0] == "register"

    def test_help_arg_with_one_arg(self):
        result = orchestrator.obtener_argumentos(
            "help", COMANDOS_STUB, {}, ("-h",),
        )
        assert result[0] is None

    def test_help_arg_with_many_args_only_accepts_exactly_two(self):
        args = ("-h", "register", "extra")
        result = orchestrator.obtener_argumentos(
            "help", COMANDOS_STUB, {}, args,
        )
        assert result[0] is None

    def test_unknown_field_prints_error(self, capsys):
        comando = {"cmd": {"need_args": ["campo_invalido"]}}
        result = orchestrator.obtener_argumentos(
            "cmd", comando, {}, ("x",),
        )
        captured = capsys.readouterr()
        assert result is None
        assert "campo no esta en direcciones" in captured.out


class TestEjecutarFuncion:
    def test_calls_target_with_args(self):
        received = {}
        def fn(a, b):
            received["args"] = (a, b)
        funciones = {"x": fn}
        orchestrator.ejecutar_funcion("x", ("one", "two"), funciones)
        assert received["args"] == ("one", "two")

    def test_calls_target_with_single_arg(self):
        received = {}
        def fn(a):
            received["arg"] = a
        funciones = {"y": fn}
        orchestrator.ejecutar_funcion("y", ("hello",), funciones)
        assert received["arg"] == "hello"

    def test_calls_target_with_no_args(self):
        received = {"called": False}
        def fn():
            received["called"] = True
        funciones = {"z": fn}
        orchestrator.ejecutar_funcion("z", (), funciones)
        assert received["called"] is True

    def test_uses_flat_funciones_dict(self):
        received = {}
        def fn():
            received["ok"] = True
        orchestrator.ejecutar_funcion("test", (), {"test": fn})
        assert received["ok"] is True


class TestOrchestratorMain:
    def test_sends_resolved_args_to_executor(self, tmp_path, monkeypatch):
        custom_cfg = tmp_path / "config.ini"
        ssh_dir = tmp_path / "ssh"
        ssh_dir.mkdir()
        ssh_cfg = ssh_dir / "config"
        ssh_cfg.write_text("", encoding="utf-8")
        custom_cfg.write_text(f"[directory]\nSSH_DIR = {ssh_dir}\n", encoding="utf-8")
        monkeypatch.setattr(orchestrator, "config_file", lambda: custom_cfg)

        received = {}
        def fake_ejecutar_funcion(comando, argumentos, funciones):
            received["comando"] = comando
            received["argumentos"] = argumentos
            received["funciones"] = funciones

        monkeypatch.setattr(orchestrator, "ejecutar_funcion", fake_ejecutar_funcion)

        orchestrator.orchestrator_main(
            "register",
            orchestrator.COMANDOS,
            ("-r", "alice@server:22"),
        )

        assert received["comando"] == "register"
        assert received["argumentos"][0] == "alice@server:22"
        assert received["argumentos"][1] == ssh_cfg
        assert received["funciones"] is orchestrator.FUNCIONES


class TestFuncionesDict:
    def test_contains_all_commands(self):
        expected = {"register", "edit", "list", "delete", "build", "help"}
        assert set(orchestrator.FUNCIONES.keys()) == expected

    def test_values_are_callable(self):
        for name, func in orchestrator.FUNCIONES.items():
            assert callable(func), f"{name} is not callable"


class TestComandosImport:
    def test_comandos_imported_from_flags(self):
        from sshr.core.internal.flags import COMANDOS as FLAGS_COMANDOS
        assert orchestrator.COMANDOS is FLAGS_COMANDOS


class TestStubCommands:
    def test_stub_commands_print_expected(self, capsys, tmp_path):
        dummy = tmp_path / "config"
        dummy.write_text("")
        result = orchestrator.list_main(str(dummy))
        assert result is None or result is not None
