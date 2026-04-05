"""
Tesseract OCR helpers for PDFs via rasterization (pdf2image).

System dependencies (macOS):
  brew install tesseract poppler

Optional extra languages:
  brew install tesseract-lang
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, List, Optional, Tuple, Union

import pytesseract
from pdf2image import convert_from_path, pdfinfo_from_path
from PIL import Image

PageResult = Tuple[int, str, Image.Image]


def project_root() -> Path:
    return Path(__file__).resolve().parent


def find_pdfs(
    root: Union[str, Path],
    *,
    recursive: bool = True,
) -> List[Path]:
    """Return sorted PDF paths under root."""
    root = Path(root).resolve()
    pattern = "**/*.pdf" if recursive else "*.pdf"
    return sorted(p for p in root.glob(pattern) if p.is_file())


def page_count(pdf_path: Union[str, Path]) -> int:
    info = pdfinfo_from_path(str(pdf_path))
    return int(info["Pages"])


def iter_ocr_pages(
    pdf_path: Union[str, Path],
    *,
    dpi: int = 200,
    lang: str = "eng",
    first_page: Optional[int] = None,
    last_page: Optional[int] = None,
) -> Iterator[PageResult]:
    """
    Yield (1-based page index, ocr_text, pil_image) for each rendered page.

    first_page / last_page are 1-based inclusive; None means start/end.
    """
    pdf_path = Path(pdf_path)
    total = page_count(pdf_path)
    fp = 1 if first_page is None else max(1, first_page)
    lp = total if last_page is None else min(total, last_page)
    if fp > lp:
        return

    images = convert_from_path(
        str(pdf_path),
        dpi=dpi,
        first_page=fp,
        last_page=lp,
    )
    for i, img in enumerate(images):
        page_num = fp + i
        text = pytesseract.image_to_string(img, lang=lang)
        yield page_num, text, img


def ocr_pdf(
    pdf_path: Union[str, Path],
    *,
    dpi: int = 200,
    lang: str = "eng",
    first_page: Optional[int] = None,
    last_page: Optional[int] = None,
) -> List[PageResult]:
    return list(
        iter_ocr_pages(
            pdf_path,
            dpi=dpi,
            lang=lang,
            first_page=first_page,
            last_page=last_page,
        )
    )


def tesseract_version() -> str:
    return str(pytesseract.get_tesseract_version())
