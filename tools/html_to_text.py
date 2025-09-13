"""
Simple utility to extract visible text from an HTML-like file.
Reads: raw/variable_guides/variable_guide_2012_html.txt
Writes: raw/txt/variable_guides_text/variable_guide_2012.txt

Uses BeautifulSoup if available; otherwise falls back to a regex-based tag stripper and html.unescape.
"""

from pathlib import Path
import re
import html

ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "raw" / "variable_guides" / "variable_guide_2012_html.txt"
OUT_DIR = ROOT / "raw" / "txt" / "variable_guides_text"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "variable_guide_2012.txt"


def extract_with_bs4(text: str) -> str:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")
    # remove script/style
    for s in soup(["script", "style"]):
        s.decompose()
    # get text
    txt = soup.get_text(separator="\n")
    # collapse multiple blank lines
    lines = [line.strip() for line in txt.splitlines()]
    lines = [l for l in lines if l]
    return "\n".join(lines)


def extract_with_regex(text: str) -> str:
    # remove script/style blocks
    text = re.sub(r"<script.*?>.*?</script>", "", text, flags=re.S|re.I)
    text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.S|re.I)
    # remove tags
    text = re.sub(r"<[^>]+>", "\n", text)
    # unescape HTML entities
    text = html.unescape(text)
    # collapse whitespace and blank lines
    lines = [line.strip() for line in text.splitlines()]
    lines = [l for l in lines if l]
    return "\n".join(lines)


def main():
    if not IN_PATH.exists():
        print("Input file not found:", IN_PATH)
        return

    raw = IN_PATH.read_text(encoding="utf-8", errors="replace")

    try:
        text = extract_with_bs4(raw)
    except Exception:
        print("bs4 not available or errored; using regex fallback")
        text = extract_with_regex(raw)

    OUT_PATH.write_text(text, encoding="utf-8")
    print("Wrote cleaned text to:", OUT_PATH)


if __name__ == "__main__":
    main()
