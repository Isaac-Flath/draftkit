# draftkit

Reusable helpers for gathering LLM context from URLs, files, PDFs, Google
documents, arXiv papers, and GitHub repositories.

## Installation

```bash
pip install draftkit
```

Browser-backed reading is optional:

```bash
pip install "draftkit[browser]"
playwright install
```

The browser extra uses Playwright's official Python package.

Local PDF OCR is also optional:

```bash
pip install "draftkit[ocr]"       # LightOnOCR with RapidOCR fallback
pip install "draftkit[lighton]"   # LightOnOCR only
pip install "draftkit[rapidocr]"  # CPU-friendly RapidOCR only
```

LightOnOCR downloads the Apache-licensed `lightonai/LightOnOCR-2-1B`
model on first use and performs best with a CUDA or Apple Silicon GPU.

## Usage

```python
import draftkit.read as rd

markdown = rd.read_link("https://example.org")
files = rd.read_dir("src", as_dict=True)
paper = rd.read_arxiv("1801.06146")
```

PDFs use native PDFium text extraction by default. Pages with missing or
clearly defective native text are rendered at 200 DPI and passed to
LightOnOCR, then to RapidOCR if LightOnOCR is unavailable or fails:

```python
text = rd.read_pdf("document.pdf")                    # automatic fallback
markdown = rd.read_pdf("document.pdf", ocr="lighton") # OCR every page
text = rd.read_pdf("document.pdf", ocr="rapidocr")    # OCR every page on CPU
text = rd.read_pdf("document.pdf", ocr=False)          # native text only
```

The automatic mode uses whichever optional OCR backends are installed. The
LightOn mode produces naturally ordered Markdown, including reconstructed
tables; RapidOCR returns recognized text lines.

Each `read_*` function accepts the location of a resource and returns either
its text or, for resources containing multiple files, a dictionary mapping
paths to contents.

See [`examples/usage.ipynb`](examples/usage.ipynb) for a notebook walkthrough.
