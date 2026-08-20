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

## Usage

```python
import draftkit.read as rd

markdown = rd.read_link("https://example.org")
files = rd.read_dir("src", as_dict=True)
paper = rd.read_arxiv("1801.06146")
```

Each `read_*` function accepts the location of a resource and returns either
its text or, for resources containing multiple files, a dictionary mapping
paths to contents.

See [`examples/usage.ipynb`](examples/usage.ipynb) for a notebook walkthrough.
