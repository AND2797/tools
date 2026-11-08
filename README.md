# tools

day to day tools I use for development 

## dnb

daily notebook. one text file per day, and opening a new day pulls yesterday's notes in under a fresh date header, so running todo lists carry forward without me copying anything.

config lives in `~/.dnbconf/config.toml`. copy `dnb/example-config.toml` there to start: `notebook_root` is where everything gets stored, `notebooks` is a list of names, each one becomes its own directory.

```
python3 dnb/daily_notebook.py list
python3 dnb/daily_notebook.py open daily_notebook
```

`open` creates today's file if it doesn't exist and opens it in `$EDITOR` (falls back to vim). files end up at `<notebook_root>/<notebook>/YYYY/MM/YYYYMMDD.txt`. needs python 3.11+ for tomllib. worth aliasing to `dnb` in your shell rc.

## scratch_file.py

opens `~/tmp/YYYYMMDD_scratch.txt` in `$EDITOR` (falls back to nvim) for quick unstructured notes.

