from pathlib import Path

import pytest

from sshr.commands.register import (
    agregar_conexion,
    parseo_de_direccion,
    register_main,
)


def test_parseo_de_direccion_user_host_port():
    result = parseo_de_direccion("alice@192.168.1.20:2200")
    assert result == {"HostName": "192.168.1.20", "User": "alice", "Port": "2200"}


def test_parseo_de_direccion_host_port():
    result = parseo_de_direccion("192.168.1.20:2200")
    assert result == {"HostName": "192.168.1.20", "Port": "2200"}


def test_parseo_de_direccion_user_host_default_port():
    result = parseo_de_direccion("alice@server")
    assert result == {"HostName": "server", "User": "alice", "Port": 22}


def test_parseo_de_direccion_invalid_non_numeric_port(capsys):
    result = parseo_de_direccion("alice@server:not-a-port")
    captured = capsys.readouterr()
    assert result is None
    assert "port must be a number" in captured.out


def test_parseo_de_direccion_invalid_empty_section(capsys):
    result = parseo_de_direccion("alice@:22")
    captured = capsys.readouterr()
    assert result is None
    assert "missing required parts" in captured.out


def test_parseo_de_direccion_invalid_multiple_arroba(capsys):
    result = parseo_de_direccion("a@b@c:22")
    captured = capsys.readouterr()
    assert result is None
    assert "too many '@'" in captured.out


def test_agregar_conexion_format():
    data = {"Host": "prod", "HostName": "10.0.0.5", "User": "root", "Port": 22}
    result = agregar_conexion(data)
    assert result == "\nHost prod\n    HostName 10.0.0.5\n    User root\n    Port 22"


def test_register_main_writes_to_config(tmp_path, monkeypatch):
    ssh_config = tmp_path / "config"
    ssh_config.write_text("", encoding="utf-8")

    inputs = iter(["mi-servidor", "1", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    register_main("alice@10.0.0.5:2200", str(ssh_config))

    content = ssh_config.read_text(encoding="utf-8")
    assert "Host mi-servidor" in content
    assert "HostName 10.0.0.5" in content
    assert "User alice" in content
    assert "Port 2200" in content


def test_register_main_cancelled_alias_does_not_crash(tmp_path, monkeypatch):
    ssh_config = tmp_path / "config"
    ssh_config.write_text("", encoding="utf-8")

    inputs = iter(["alias-temp", "n", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    register_main("alice@10.0.0.5:2200", str(ssh_config))
