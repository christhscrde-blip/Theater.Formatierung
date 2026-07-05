from __future__ import annotations

import subprocess
import sys
import tomllib
import zipfile
from importlib.metadata import EntryPoint
from pathlib import Path

import build_backend


def test_pyproject_registers_console_script():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["build-system"]["requires"] == []
    assert pyproject["build-system"]["build-backend"] == "build_backend"
    assert pyproject["project"]["name"] == "theater-formatierung"
    assert pyproject["project"]["scripts"]["theater-formatierung"] == "src.cli:main"


def test_console_script_entry_point_loads_existing_cli():
    entry_point = EntryPoint(
        name="theater-formatierung",
        value="src.cli:main",
        group="console_scripts",
    )

    loaded = entry_point.load()

    assert loaded.__module__ == "src.cli"
    assert loaded.__name__ == "main"


def test_existing_cli_help_is_invokable_as_packaging_smoke_test():
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "theater-formatierung" in result.stdout
    assert "analyse" in result.stdout


def test_editable_wheel_contains_console_entry_point(tmp_path: Path):
    wheel_name = build_backend.build_editable(tmp_path)

    with zipfile.ZipFile(tmp_path / wheel_name) as wheel:
        names = set(wheel.namelist())
        entry_points = wheel.read(
            "theater_formatierung-0.1.0a1.dist-info/entry_points.txt"
        ).decode()

    assert "theater_formatierung_editable.pth" in names
    assert "theater-formatierung = src.cli:main" in entry_points
