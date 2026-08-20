# Release notes

## 0.2.0

### New features

- Read native PDF text with PDFium.
- Automatically OCR scanned or defective pages with optional LightOnOCR and
  RapidOCR backends.
- Allow forcing LightOnOCR Markdown or RapidOCR text extraction for every
  page.

## 0.1.1

### Dependencies

- Replace `toolslm` with local HTML selection and Markdown conversion.
- Replace `playwrightnb` with the official, optional `playwright` package.
- Remove the remaining dependency paths to `python-fasthtml`, `fastcore`, and
  `llms-txt`.

## 0.1.0

### Breaking changes

- Rename the distribution and import package from `contextkit` to `draftkit`.
- Make Python modules under `src/draftkit` the source of truth; notebooks are
  now examples only.
- Move browser automation support to the optional `browser` extra.

## 0.0.10

### Breaking changes

- Rename read_url to read_link ([#12](https://github.com/AnswerDotAI/ContextKit/pull/12)), thanks to [@algal](https://github.com/algal)


## 0.0.9

### New Features

- Adds docments-style comments to existing functions, so they can be used with SolveIt tool-calling if desired.

- add read_text ([#9](https://github.com/AnswerDotAI/ContextKit/issues/9))

- pypdf2 has moved to pypdf ([#7](https://github.com/AnswerDotAI/ContextKit/pull/7)), thanks to [@RensDimmendaal](https://github.com/RensDimmendaal)
  - This PR renames dependency `PyPDF2` to `pypdf` as the maintainers moved that package.
This move will silence the deprecation warning that's currently shown when using contextkit.

> .venv/lib/python3.12/site-packages/PyPDF2/__init__.py:21: DeprecationWarning: PyPDF2 is deprecated. Please move to the pypdf library instead.

See: https://pypi.org/project/PyPDF2/

### Bugs Squashed

- Fixes read_arxiv to use HTTPS, and adds docments docs to various functions for tool support ([#10](https://github.com/AnswerDotAI/ContextKit/pull/10)), thanks to [@algal](https://github.com/algal)
  - - Arxiv.org started returning a 301 when you visit their HTTP URL. Commit fdfc490 fixes this library to use HTTPS, restoring lost functionality


## 0.0.8

### New Features

- pypdf2 has moved to pypdf ([#7](https://github.com/AnswerDotAI/ContextKit/pull/7)), thanks to [@RensDimmendaal](https://github.com/RensDimmendaal)
  - This PR renames dependency `PyPDF2` to `pypdf` as the maintainers moved that package.
This move will silence the deprecation warning that's currently shown when using contextkit.

> .venv/lib/python3.12/site-packages/PyPDF2/__init__.py:21: DeprecationWarning: PyPDF2 is deprecated. Please move to the pypdf library instead.

See: https://pypi.org/project/PyPDF2/



## 0.0.7

- Update to dependencies


## 0.0.6

- Make read_gh_repo default to returning dict

## 0.0.5

- Bug fix in __init__ for read_gh_repo


## 0.0.4




## 0.0.2

### New Features

- Release Context Kit ([#5](https://github.com/AnswerDotAI/ContextKit/issues/5))
