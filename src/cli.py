from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .classifier import build_report, classify_docx
from .report import write_analysis_report, write_classification_csv


def analyse_command(args: argparse.Namespace) -> int:
    docx_path = Path(args.docx)
    paragraphs = classify_docx(docx_path)
    report = build_report(docx_path, paragraphs)

    out_dir = Path(args.out)
    report_path = write_analysis_report(report, out_dir)
    csv_path = write_classification_csv(paragraphs, out_dir)

    print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
    print(f"Analysebericht: {report_path}")
    print(f"Absatzklassifikation: {csv_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="theater-formatierung")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyse = subparsers.add_parser("analyse", help="DOCX analysieren und Berichte schreiben")
    analyse.add_argument("docx", help="Pfad zur DOCX-Datei")
    analyse.add_argument("--out", default="reports", help="Ausgabeordner für Berichte")
    analyse.set_defaults(func=analyse_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
