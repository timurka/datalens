from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = Path("/Users/timur/.codex/skills/datalens")
SRC = SKILL_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

default_config = ROOT / "datalens-sync.json"
if "--config" not in sys.argv[1:] and default_config.exists():
    sys.argv[1:1] = ["--config", str(default_config)]

from datalens_sync_repo.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
