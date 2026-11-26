"""Build a single offline rehearsal file from the shared overlay UI."""
from pathlib import Path
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 build_rehearsal.py OUTPUT.html")
    source = Path(__file__).with_name("overlay.html")
    html = source.read_text(encoding="utf-8")
    marker = '<html lang="en" data-feed="preview">'
    if html.count(marker) != 1:
        raise SystemExit("Expected one preview-mode marker in overlay.html")
    target = Path(sys.argv[1])
    if target.resolve() == source.resolve():
        raise SystemExit("Choose a separate output file.")
    target.write_text(html.replace(marker, marker.replace("preview", "rehearsal")), encoding="utf-8")
