"""Console entry point: start the PlantMemory hub and open the browser.

Installed as the ``plantmemory`` command (see pyproject.toml). Running it with no
arguments starts the local hub and opens the dashboard in your browser.
"""
from __future__ import annotations

import argparse

from .hub import run_hub


def main() -> None:
    ap = argparse.ArgumentParser(
        prog="plantmemory",
        description="PlantMemory — knowledge continuity + Management of Change hub.",
    )
    ap.add_argument("--port", type=int, default=7700, help="port to serve on (default 7700)")
    ap.add_argument("--host", default=None, help="bind host (default 127.0.0.1; use 0.0.0.0 in a container)")
    ap.add_argument("--no-open", action="store_true", help="do not open a browser window")
    a = ap.parse_args()
    run_hub(port=a.port, open_browser=not a.no_open, host=a.host)


if __name__ == "__main__":
    main()
