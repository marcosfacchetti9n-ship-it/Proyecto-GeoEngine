from __future__ import annotations

import argparse

from geoengine.app import launch_app
from geoengine.report import build_portfolio_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GeoEngine demo runner")
    parser.add_argument("--report", action="store_true", help="Imprime un resumen headless del motor")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.report:
        print(build_portfolio_report())
        return
    launch_app()


if __name__ == "__main__":
    main()
