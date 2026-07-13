from sshr.commands.build import build_main


def test_build_main_creates_required_structure(tmp_path, monkeypatch, capsys):
    home = tmp_path / "home"
    home.mkdir()

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)

    build_main()
    capsys.readouterr()

    global_config = home / ".config"
    sshr_config_dir = global_config / "sshr"
    sshr_config_file = sshr_config_dir / "config.ini"
    ssh_dir = home / ".ssh"
    ssh_config_file = ssh_dir / "config"

    assert global_config.is_dir()
    assert sshr_config_dir.is_dir()
    assert sshr_config_file.is_file()
    assert ssh_dir.is_dir()
    assert ssh_config_file.is_file()
