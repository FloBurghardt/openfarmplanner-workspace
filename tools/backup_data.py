"""Back up the farm data folder (SQLite database + media) into a dated folder, e.g. on the SMB share.

Uses SQLite's backup API, so it is safe while the app is running (WAL included). The live
data folder itself must stay on a local disk: SQLite's WAL mode does not work over network
file systems.

  uv run tools/backup_data.py <data-folder> <backup-root>
  uv run tools/backup_data.py ../OpenFarmPlanner_data //nas/backup/openfarmplanner

Restore on another machine: copy `db.sqlite3` and `media/` of the newest dated folder into
that machine's data folder (backend stopped), then point SQLITE_PATH / MEDIA_ROOT at it.
"""

import datetime
import shutil
import sqlite3
import sys
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(__doc__)
data, root = Path(sys.argv[1]), Path(sys.argv[2])
target = root / datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
target.mkdir(parents=True)

src, dst = sqlite3.connect(data / "db.sqlite3"), sqlite3.connect(target / "db.sqlite3")
src.backup(dst)
src.close()
check = dst.execute("pragma integrity_check").fetchone()[0]
dst.close()
if check != "ok":
    sys.exit(f"integrity check of the copy failed: {check}")

if (data / "media").is_dir():
    shutil.copytree(data / "media", target / "media")
print(f"backup written to {target} (integrity ok)")
