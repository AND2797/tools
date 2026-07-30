# tools

small tools I use day to day. mostly note taking, plus some git helpers I keep meaning to write.

## dnb

daily notebook. one text file per day, and opening a new day pulls yesterday's notes in under a fresh date header, so running todo lists carry forward without me copying anything.

config lives in `~/.dnbconf/config.toml`. copy `dnb/example-config.toml` there to start: `notebook_root` is where everything gets stored, `notebooks` is a list of names, each one becomes its own directory.

```
python3 dnb/daily_notebook.py list
python3 dnb/daily_notebook.py open daily_notebook
```

`open` creates today's file if it doesn't exist and opens it in `$EDITOR` (falls back to vim). files end up at `<notebook_root>/<notebook>/YYYY/MM/YYYYMMDD.txt`. needs python 3.11+ for tomllib. worth aliasing to `dnb` in your shell rc.

## scratch_file.py

simpler version of the same idea, no config and no rollover. opens `~/tmp/YYYYMMDD_scratch.txt` in `$EDITOR` (falls back to nvim) for quick unstructured notes.

## git-scripts

nothing usable here yet. `wishlist.txt` has the ideas (dumping a file's contents from different hashes/branches, quick rebases) and `diff_dump.py` is a stub for the first one.
