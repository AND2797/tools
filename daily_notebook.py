#!/usr/bin/env python3
"""dnb: daily notebook.

A small CLI for keeping daily notes. Creates a text file named YYYYMMDD.txt
under a YYYY/MM/ directory per notebook. Opening a new day rolls over the
previous day's contents beneath a fresh date header.
"""

import os
import re
import subprocess
import sys
import tomllib
from datetime import date, datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".dnbconf" / "config.toml"
HEADER_FMT = "%A, %B %-d, %Y"  # for writing, e.g. "Saturday, July 18, 2026"
HEADER_PARSE_FMT = "%A, %B %d, %Y"  # for reading; strptime rejects the %-d flag
DATE_FILE_RE = re.compile(r"(\d{8})\.txt$")


def load_config():
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
    return config["notebook_root"], config["notebooks"]


def editor():
    """$EDITOR split into command + args (may include flags), default vim."""
    return os.environ.get("EDITOR", "").split() or ["vim"]


def strip_header(content):
    """Drop a leading date-header line so headers don't stack across rollovers."""
    line, _, rest = content.partition("\n")
    try:
        datetime.strptime(line.strip(), HEADER_PARSE_FMT)
    except ValueError:
        return content  # first line isn't a header, leave it alone
    return rest


def find_latest_file(notebook_path, before):
    """Most recent YYYYMMDD.txt strictly before `before`, or None."""
    latest_path, latest_date = None, None
    for path in notebook_path.rglob("*.txt"):
        m = DATE_FILE_RE.search(path.name)
        if not m:
            continue
        try:
            file_date = datetime.strptime(m.group(1), "%Y%m%d").date()
        except ValueError:
            continue
        if file_date >= before:
            continue
        if latest_date is None or file_date > latest_date:
            latest_path, latest_date = path, file_date
    return latest_path


def open_notebook(notebook, notebook_root, notebooks):
    """Resolve today's file, creating it (with rollover) if it doesn't exist."""
    if notebook not in notebooks:
        raise ValueError(f"notebook {notebook!r} doesn't exist")

    notebook_path = Path(notebook_root).expanduser() / notebook
    today = date.today()

    day_dir = notebook_path / today.strftime("%Y") / today.strftime("%m")
    day_dir.mkdir(parents=True, exist_ok=True)
    todays_file = day_dir / (today.strftime("%Y%m%d") + ".txt")

    if not todays_file.exists():
        prev = find_latest_file(notebook_path, today)
        if prev is None:
            todays_file.touch()
        else:
            print(f"Rolling over from {prev}")
            header = today.strftime(HEADER_FMT) + " \n"
            todays_file.write_text(header + strip_header(prev.read_text()))

    return todays_file


def main(argv):
    try:
        notebook_root, notebooks = load_config()
    except (OSError, tomllib.TOMLDecodeError, KeyError) as e:
        sys.exit(f"Error: reading config {CONFIG_PATH}: {e}")

    if not argv:
        sys.exit("usage: dnb <list|open <notebook>>")

    if argv[0] == "list":
        print("Notebooks:")
        for nb in notebooks:
            print(f"- {nb}")
    elif argv[0] == "open":
        if len(argv) < 2:
            sys.exit("usage: dnb open <notebook>")
        try:
            path = open_notebook(argv[1], notebook_root, notebooks)
        except ValueError as e:
            sys.exit(f"Error: {e}")
        subprocess.run([*editor(), str(path)])
    else:
        sys.exit(f"Error: unknown command {argv[0]!r}")


if __name__ == "__main__":
    main(sys.argv[1:])
