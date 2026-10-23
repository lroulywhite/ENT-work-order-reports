#!/usr/bin/env python3
"""Build the simulation from the approved snapshot.

Verifies every checksum in MANIFEST.json first and stops on any mismatch
(snapshot-spec.md, "Verifying checksums"). Then embeds the captures, unmodified,
into src/template.html and writes one self-contained HTML file to simulations/.

Usage:  python3 src/build.py
"""
import base64, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "assets" / "snapshots" / "enterprise-2026-10-v1"
OUT = ROOT / "simulations" / "ENT _ Run a Work Order Report [Simulation].html"

# Order matters: template.html refers to these by index.
SCREENS = [
    "work-orders-list__row-selected",       # 0
    "work-orders-list__actions-menu",       # 1
    "work-order-reports__list",             # 2
    "work-order-reports__selected",         # 3
    "report-prompt__default",               # 4
    "report-viewer__default",               # 5
    "report-viewer__tools-menu",            # 6
    "report-viewer__email-options-menu",    # 7
]

def verify() -> None:
    m = json.loads((SNAP / "MANIFEST.json").read_text())
    if m.get("mock_data_confirmed_safe") is not True:
        sys.exit("STOP: mock_data_confirmed_safe is not true in MANIFEST.json")
    bad = [p for p, want in m["files"].items()
           if not (SNAP / p).exists() or hashlib.sha256((SNAP / p).read_bytes()).hexdigest() != want]
    if bad:
        sys.exit(f"STOP: checksum mismatch or missing file: {bad}")
    print("Snapshot OK:", m["snapshot_id"])

def main() -> None:
    verify()
    imgs = ["data:image/png;base64," + base64.b64encode((SNAP / "screens" / f"{s}.png").read_bytes()).decode()
            for s in SCREENS]
    html = (ROOT / "src" / "template.html").read_text()
    assert "/*IMGS*/[]" in html, "placeholder missing from template.html"
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html.replace("/*IMGS*/[]", json.dumps(imgs)))
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
