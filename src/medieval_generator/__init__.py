"""Medieval narrative content generator package."""

from __future__ import annotations

from typing import Any, Dict, List


def build_argument_parser():
    """Return the CLI argument parser."""

    from .cli import build_argument_parser as _build_argument_parser

    return _build_argument_parser()


def main(argv: List[str] | None = None) -> Dict[str, Any]:
    """Entry point for the console script."""

    from .cli import main as _cli_main

    return _cli_main(argv)


__all__ = ["build_argument_parser", "main"]
