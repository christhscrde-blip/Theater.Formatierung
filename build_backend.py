from __future__ import annotations

import base64
import csv
import hashlib
import zipfile
from pathlib import Path

PROJECT_NAME = "theater-formatierung"
VERSION = "0.1.0a1"
DIST_INFO = "theater_formatierung-0.1.0a1.dist-info"
WHEEL_NAME = "theater_formatierung-0.1.0a1-py3-none-any.whl"


def get_requires_for_build_wheel(config_settings=None):
    return []


def get_requires_for_build_editable(config_settings=None):
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    return _write_metadata(Path(metadata_directory))


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
    return _write_metadata(Path(metadata_directory))


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    wheel_path = Path(wheel_directory) / WHEEL_NAME
    project_root = Path(__file__).resolve().parent
    files: dict[str, bytes] = {}
    _add_project_file(files, project_root, "README.md")
    for package_dir in ("src", "styles"):
        for path in sorted((project_root / package_dir).rglob("*")):
            if path.is_file():
                _add_project_file(
                    files, project_root, path.relative_to(project_root).as_posix()
                )
    _add_dist_info(files, editable=False)
    _write_wheel(wheel_path, files)
    return wheel_path.name


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    wheel_path = Path(wheel_directory) / WHEEL_NAME
    files = {
        "theater_formatierung_editable.pth": (
            f"{Path(__file__).resolve().parent}\n".encode()
        ),
    }
    _add_dist_info(files, editable=True)
    _write_wheel(wheel_path, files)
    return wheel_path.name


def _write_metadata(metadata_directory: Path) -> str:
    dist_info = metadata_directory / DIST_INFO
    dist_info.mkdir(parents=True, exist_ok=True)
    (dist_info / "METADATA").write_bytes(_metadata())
    (dist_info / "WHEEL").write_bytes(_wheel_metadata())
    (dist_info / "entry_points.txt").write_bytes(_entry_points())
    return DIST_INFO


def _add_project_file(
    files: dict[str, bytes], project_root: Path, relative_path: str
) -> None:
    files[relative_path] = (project_root / relative_path).read_bytes()


def _add_dist_info(files: dict[str, bytes], editable: bool) -> None:
    files[f"{DIST_INFO}/METADATA"] = _metadata()
    files[f"{DIST_INFO}/WHEEL"] = _wheel_metadata()
    files[f"{DIST_INFO}/entry_points.txt"] = _entry_points()
    files[f"{DIST_INFO}/direct_url.json"] = _direct_url(editable)


def _metadata() -> bytes:
    return (
        "Metadata-Version: 2.4\n"
        f"Name: {PROJECT_NAME}\n"
        f"Version: {VERSION}\n"
        "Summary: DOCX analysis and formatting tools for theater manuscripts "
        "with visible-text integrity checks.\n"
        "Requires-Python: >=3.11\n"
        "Requires-Dist: python-docx>=1.1.2\n"
        "Provides-Extra: dev\n"
        "Requires-Dist: pytest>=8.0.0; extra == 'dev'\n"
        "\n"
    ).encode()


def _wheel_metadata() -> bytes:
    return (
        "Wheel-Version: 1.0\n"
        "Generator: theater-formatierung-build-backend\n"
        "Root-Is-Purelib: true\n"
        "Tag: py3-none-any\n"
        "\n"
    ).encode()


def _entry_points() -> bytes:
    return b"[console_scripts]\ntheater-formatierung = src.cli:main\n"


def _direct_url(editable: bool) -> bytes:
    root_uri = Path(__file__).resolve().parent.as_uri()
    editable_text = "true" if editable else "false"
    return (
        f'{{"dir_info": {{"editable": {editable_text}}}, "url": "{root_uri}"}}\n'
        .encode()
    )


def _write_wheel(wheel_path: Path, files: dict[str, bytes]) -> None:
    record_path = f"{DIST_INFO}/RECORD"
    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as wheel:
        record_rows = []
        for archive_path, content in sorted(files.items()):
            wheel.writestr(archive_path, content)
            record_rows.append((archive_path, _hash(content), str(len(content))))
        record_rows.append((record_path, "", ""))
        wheel.writestr(record_path, _record_content(record_rows))


def _hash(content: bytes) -> str:
    digest = hashlib.sha256(content).digest()
    encoded = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return f"sha256={encoded}"


def _record_content(rows: list[tuple[str, str, str]]) -> str:
    from io import StringIO

    handle = StringIO()
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerows(rows)
    return handle.getvalue()
