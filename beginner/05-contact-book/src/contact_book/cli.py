"""Command-line interface: argument parsing and input/output only."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .errors import ContactError
from .export import export_to_csv
from .models import Contact
from .service import (
    create_contact,
    delete_contact,
    find_contacts,
    update_contact,
)
from .storage import load_contacts, save_contacts

DEFAULT_DATA_FILE = Path("contacts.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="contact-book", description="A simple local contact book."
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help=f"path to the JSON data file (default: {DEFAULT_DATA_FILE})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="add a contact")
    add.add_argument("--name", required=True)
    add.add_argument("--email", default=None)
    add.add_argument("--phone", default=None)

    subparsers.add_parser("list", help="list all contacts")

    search = subparsers.add_parser("search", help="search contacts")
    search.add_argument("query")

    update = subparsers.add_parser("update", help="update a contact by id")
    update.add_argument("id")
    update.add_argument("--name", default=None)
    update.add_argument("--email", default=None)
    update.add_argument("--phone", default=None)

    delete = subparsers.add_parser("delete", help="delete a contact by id")
    delete.add_argument("id")

    export = subparsers.add_parser("export", help="export contacts to CSV")
    export.add_argument("path", type=Path)
    export.add_argument(
        "--force", action="store_true", help="overwrite the file if it exists"
    )

    return parser


def _print_contacts(contacts: list[Contact]) -> None:
    if not contacts:
        print("No contacts found.")
        return
    print(f"{'ID':10}  {'NAME':24}  {'EMAIL':28}  PHONE")
    for contact in contacts:
        print(
            f"{contact.id:10}  {contact.name:24}  "
            f"{contact.email or '-':28}  {contact.phone or '-'}"
        )


def _run_add(args: argparse.Namespace) -> int:
    contacts = load_contacts(args.data_file)
    contact = create_contact(name=args.name, email=args.email, phone=args.phone)
    contacts.append(contact)
    save_contacts(args.data_file, contacts)
    print(f"Added contact {contact.id}: {contact.name}")
    return 0


def _run_list(args: argparse.Namespace) -> int:
    _print_contacts(load_contacts(args.data_file))
    return 0


def _run_search(args: argparse.Namespace) -> int:
    _print_contacts(find_contacts(load_contacts(args.data_file), args.query))
    return 0


def _run_update(args: argparse.Namespace) -> int:
    contacts = load_contacts(args.data_file)
    updated_list, contact = update_contact(
        contacts, args.id, name=args.name, email=args.email, phone=args.phone
    )
    save_contacts(args.data_file, updated_list)
    print(f"Updated contact {contact.id}: {contact.name}")
    return 0


def _run_delete(args: argparse.Namespace) -> int:
    contacts = load_contacts(args.data_file)
    remaining = delete_contact(contacts, args.id)
    save_contacts(args.data_file, remaining)
    print(f"Deleted contact {args.id}.")
    return 0


def _run_export(args: argparse.Namespace) -> int:
    contacts = load_contacts(args.data_file)
    export_to_csv(contacts, args.path, force=args.force)
    print(f"Exported {len(contacts)} contact(s) to {args.path}")
    return 0


_COMMANDS = {
    "add": _run_add,
    "list": _run_list,
    "search": _run_search,
    "update": _run_update,
    "delete": _run_delete,
    "export": _run_export,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    handler = _COMMANDS[args.command]
    try:
        return handler(args)
    except ContactError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
