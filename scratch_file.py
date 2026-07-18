# This scripts open a scratch text file in $HOMEDIR/tmp/scratch_YYYMMDD.txt
# Use this to store quick unstructured notes for the day

import os
from subprocess import run
from pathlib import Path
from datetime import datetime

home_dir = Path.home()
temp_dir = Path.joinpath(home_dir, "tmp")
temp_dir.mkdir(exist_ok=True)

curr_date = datetime.now().strftime("%Y%m%d")
file = temp_dir.joinpath(f"{curr_date}_scratch.txt")
file.touch()

editor = os.getenv("EDITOR", "nvim")

run([editor, str(file)])
