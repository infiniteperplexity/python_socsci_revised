"""
Small utility to convert all PDFs in raw/variable_guides to text files in raw/txt/variable_guides_text.
It prefers PyMuPDF (fitz). If not installed, it will try to use the system `pdftotext` command.

Usage:
    python tools/pdf_to_text.py

Outputs:
    raw/txt/variable_guides_text/<original_basename>.txt
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "raw" / "variable_guides"
OUT_DIR = ROOT / "raw" / "txt" / "variable_guides_text"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_with_pymupdf(pdf_path: Path) -> str:
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)
    texts = []
    for page in doc:
        texts.append(page.get_text())
    return "\n".join(texts)


def extract_with_pdftotext(pdf_path: Path) -> str:
    # Use system pdftotext if available. Write to a temp file and read.
    import subprocess
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmpname = tmp.name
    try:
        subprocess.check_call(["pdftotext", str(pdf_path), tmpname])
        with open(tmpname, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    finally:
        try:
            os.unlink(tmpname)
        except Exception:
            pass


def main():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print("No PDFs found in", PDF_DIR)
        return

    use_pymupdf = True
    try:
        import fitz
    except Exception:
        use_pymupdf = False

    if not use_pymupdf:
        print("PyMuPDF (fitz) not found. Will try system pdftotext.")

    for p in pdfs:
        out_path = OUT_DIR / (p.stem + ".txt")
        print("Processing:", p.name, "->", out_path)
        try:
            if use_pymupdf:
                text = extract_with_pymupdf(p)
            else:
                text = extract_with_pdftotext(p)
        except Exception as e:
            print("Failed to extract", p, "because:", e)
            continue

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)

    print("Done. Text files written to", OUT_DIR)


if __name__ == "__main__":
    main()
