"""Entry point for the news-image-20261120 make.fun entry.

The poster (entry.png, beside this file) is drawn at build time by
draw.py from the verified news of Friday 20 November 2026. The grading
sandbox runs this program with no network and no third-party packages,
so all it does is copy the finished PNG, byte for byte, to the output
directory: /output, or $MAKEFUN_OUTPUT_DIR when that is set. Running it
twice writes identical bytes.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"entry image missing: {SOURCE}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
