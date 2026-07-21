"""Command-line interface for the password generator.

Generated passwords are written to stdout only; they are never logged.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .errors import PolicyError
from .generator import generate_passwords
from .policy import MAX_LENGTH, MIN_LENGTH, Policy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password-generator",
        description="Generate strong random passwords.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--length",
        type=int,
        default=16,
        help=f"password length ({MIN_LENGTH}-{MAX_LENGTH}, default: 16)",
    )
    parser.add_argument(
        "--count", type=int, default=1, help="how many passwords to generate"
    )
    parser.add_argument(
        "--no-lowercase", action="store_true", help="exclude lowercase letters"
    )
    parser.add_argument(
        "--no-uppercase", action="store_true", help="exclude uppercase letters"
    )
    parser.add_argument("--no-digits", action="store_true", help="exclude digits")
    parser.add_argument(
        "--symbols", action="store_true", help="include punctuation symbols"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    policy = Policy(
        length=args.length,
        use_lowercase=not args.no_lowercase,
        use_uppercase=not args.no_uppercase,
        use_digits=not args.no_digits,
        use_symbols=args.symbols,
    )
    try:
        passwords = generate_passwords(policy, args.count)
    except PolicyError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    for password in passwords:
        print(password)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
