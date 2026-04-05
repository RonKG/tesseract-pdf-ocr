# test_ocr_inputs

Small local workspace to **run Tesseract OCR on PDFs**. Each page is rasterized with [pdf2image](https://github.com/Belval/pdf2image) (needs Poppler), then passed to [Tesseract](https://github.com/tesseract-ocr/tesseract) via [pytesseract](https://github.com/madmaze/pytesseract).

Typical use: try OCR settings (DPI, language, page range) on scans or gazette-style PDFs before wiring the same stack into other tools.

## What is in this repo

| Item | Role |
|------|------|
| `ocr_tesseract_demo.ipynb` | Jupyter walkthrough: environment checks, PDF picker, and interactive OCR |
| `ocr_tesseract_pdf.py` | Reusable helpers (`find_pdfs`, `page_count`, `ocr_pdf`, `iter_ocr_pages`) |
| `requirements.txt` | Python dependencies |

## Getting started

### 1. System tools (macOS)

Tesseract and Poppler are **not** installed by pip. Install once (for example with Homebrew):

```bash
brew install tesseract poppler
# optional: extra Tesseract language packs
brew install tesseract-lang
```

### 2. Python virtual environment

Use Python 3.11+ if you can (Apple’s default `python3` is often older).

```bash
cd /path/to/test_ocr_inputs
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Optional: register this environment as a Jupyter kernel so the notebook uses `.venv` automatically:

```bash
python -m ipykernel install --user --name=test_ocr_inputs --display-name="Python (test_ocr_inputs)"
```

### 3. Add PDFs

Put `.pdf` files **anywhere under this project folder** (recursively). The notebook discovers them automatically.

## How to use it

### Jupyter notebook (recommended)

1. Activate `.venv` and start Jupyter from the project directory, or open `ocr_tesseract_demo.ipynb` in Cursor/VS Code and select the **Python (test_ocr_inputs)** kernel (or the interpreter `.venv/bin/python`).
2. Run the cells from the top: they install deps into the active kernel, verify `tesseract` and `pdfinfo`, then show a small UI (PDF dropdown, DPI, Tesseract language, page range, **Run OCR**).
3. Adjust DPI and language (for example `eng` or `swa` if installed), choose pages, and run OCR. Output shows each page image and the extracted text.

### From Python

Import the helpers and call `ocr_pdf` (or `iter_ocr_pages`) with a path to your PDF:

```python
from ocr_tesseract_pdf import ocr_pdf

for page_num, text, img in ocr_pdf("path/to/file.pdf", dpi=200, lang="eng", first_page=1, last_page=3):
    print(page_num, text[:200])
```

See `ocr_tesseract_pdf.py` for `find_pdfs`, `page_count`, and full argument behavior.
