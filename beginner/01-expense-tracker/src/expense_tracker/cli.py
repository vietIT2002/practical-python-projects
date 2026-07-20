"""Command-line interface: argument parsing and input/output only.

All calculations live in :mod:`expense_tracker.services`; this module just wires
the terminal to that logic and turns domain errors into exit codes.

Exit codes:

- ``0`` success
- ``1`` a domain error (invalid input, not found, or a storage problem)
- ``2`` a usage error (handled by :mod:`argparse`)
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from . import __version__
from .errors import ExpenseError
from .services import (
    create_expense,
    delete_expense,
    filter_expenses,
    summarise,
)
from .storage import load_expenses, save_expenses

DEFAULT_DATA_FILE = Path("expenses.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Track expenses from the command line.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help=f"path to the JSON data file (default: {DEFAULT_DATA_FILE})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="add an expense")
    add.add_argument("--amount", required=True, help="positive amount, e.g. 12.50")
    add.add_argument("--category", required=True, help="expense category")
    add.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="ISO date YYYY-MM-DD (default: today)",
    )
    add.add_argument("--note", default=None, help="optional note")

    listing = subparsers.add_parser("list", help="list expenses")
    listing.add_argument("--month", default=None, help="filter by month YYYY-MM")
    listing.add_argument("--category", default=None, help="filter by category")

    summary = subparsers.add_parser("summary", help="totals by month and category")
    summary.add_argument("--month", default=None, help="filter by month YYYY-MM")

    delete = subparsers.add_parser("delete", help="delete an expense by id")
    delete.add_argument("id", help="the expense id to delete")

    return parser


def _run_add(args: argparse.Namespace) -> int:
    expenses = load_expenses(args.data_file)
    expense = create_expense(
        amount=args.amount,
        category=args.category,
        on_date=args.date,
        note=args.note,
    )
    expenses.append(expense)
    save_expenses(args.data_file, expenses)
    print(
        f"Added expense {expense.id}: {expense.amount} {expense.category} "
        f"on {expense.date.isoformat()}"
    )
    return 0


def _run_list(args: argparse.Namespace) -> int:
    expenses = filter_expenses(
        load_expenses(args.data_file), month=args.month, category=args.category
    )
    if not expenses:
        print("No expenses found.")
        return 0
    print(f"{'ID':8}  {'DATE':10}  {'AMOUNT':>10}  CATEGORY")
    for expense in expenses:
        line = (
            f"{expense.id:8}  {expense.date.isoformat():10}  "
            f"{expense.amount:>10}  {expense.category}"
        )
        if expense.note:
            line += f"  ({expense.note})"
        print(line)
    return 0


def _run_summary(args: argparse.Namespace) -> int:
    expenses = load_expenses(args.data_file)
    if args.month:
        expenses = filter_expenses(expenses, month=args.month)
    summary = summarise(expenses)
    print(f"Total: {summary.total}")
    if summary.by_month:
        print("\nBy month:")
        for month, amount in summary.by_month.items():
            print(f"  {month}  {amount:>10}")
    if summary.by_category:
        print("\nBy category:")
        for category, amount in summary.by_category.items():
            print(f"  {category:15}  {amount:>10}")
    return 0


def _run_delete(args: argparse.Namespace) -> int:
    expenses = load_expenses(args.data_file)
    remaining = delete_expense(expenses, args.id)
    save_expenses(args.data_file, remaining)
    print(f"Deleted expense {args.id}.")
    return 0


_COMMANDS = {
    "add": _run_add,
    "list": _run_list,
    "summary": _run_summary,
    "delete": _run_delete,
}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = _COMMANDS[args.command]
    try:
        return handler(args)
    except ExpenseError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
