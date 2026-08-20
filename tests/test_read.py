import types

import pytest

import draftkit
import draftkit.read as rd


def test_public_api_includes_read_text():
    assert draftkit.read_text is rd.read_text
    assert "read_text" in draftkit.__all__


def test_read_file_and_directory(tmp_path):
    (tmp_path / "one.txt").write_text("one")
    (tmp_path / "two.md").write_text("two")

    assert rd.read_file(tmp_path / "one.txt") == "one"
    assert rd.read_dir(tmp_path, as_dict=True) == {
        str(tmp_path / "one.txt"): "one",
        str(tmp_path / "two.md"): "two",
    }


def test_read_gist_uses_raw_url(monkeypatch):
    response = types.SimpleNamespace(text="gist contents")
    get = lambda url: response
    monkeypatch.setattr(rd.httpx, "get", get)

    assert rd.read_gist("https://gist.github.com/user/abc123") == "gist contents"
    assert rd.read_gist("https://example.org/not-a-gist") is None


def test_read_url_delegates_with_deprecation_warning(monkeypatch):
    monkeypatch.setattr(rd, "read_link", lambda *args, **kwargs: (args, kwargs))

    with pytest.deprecated_call(match="use read_link"):
        assert rd.read_url("https://example.org", sel="main") == (
            ("https://example.org",),
            {"sel": "main"},
        )


def test_read_link_converts_selected_html(monkeypatch):
    response = types.SimpleNamespace(
        text='''
            <main><a href="https://example.org">Example</a><img src="image.png"></main>
            <aside>Not selected</aside>
        '''
    )
    monkeypatch.setattr(rd.httpx, "get", lambda url: response)

    markdown = rd.read_link("https://example.org", sel="main")

    assert "[Example](https://example.org)" in markdown
    assert "Not selected" not in markdown
    assert "image.png" not in markdown


def test_read_link_can_ignore_links(monkeypatch):
    response = types.SimpleNamespace(text='<a href="https://example.org">Example</a>')
    monkeypatch.setattr(rd.httpx, "get", lambda url: response)

    markdown = rd.read_link("https://example.org", ignore_links=True)

    assert "Example" in markdown
    assert "https://example.org" not in markdown


def test_heavy_reader_defaults_to_body(monkeypatch):
    html = '<html><body><main>Rendered content</main></body></html>'
    monkeypatch.setattr(rd, "_render_html", lambda url: html)

    assert rd.read_link("https://example.org", heavy=True).strip() == "Rendered content"


def test_heavy_reader_uses_selector(monkeypatch):
    html = '<body><main>Selected</main><aside>Skipped</aside></body>'
    monkeypatch.setattr(rd, "_render_html", lambda url: html)

    markdown = rd.read_link("https://example.org", heavy=True, sel="main")

    assert markdown.strip() == "Selected"


def test_read_pdf_extracts_pages_with_pdfium(monkeypatch):
    closed = []

    class TextPage:
        def __init__(self, text):
            self.text = text

        def get_text_bounded(self):
            return self.text

        def close(self):
            closed.append(self.text)

    class Page:
        def __init__(self, text):
            self.text = text

        def get_textpage(self):
            return TextPage(self.text)

        def close(self):
            closed.append(f"page: {self.text}")

    class Document:
        def __init__(self, path):
            assert path == "document.pdf"
            self.pages = [Page("First page"), Page("Second page")]

        def __len__(self):
            return len(self.pages)

        def __getitem__(self, index):
            return self.pages[index]

        def close(self):
            closed.append("document")

    monkeypatch.setattr(rd.pdfium, "PdfDocument", Document)

    assert rd.read_pdf("document.pdf", ocr=False) == "First page\n\nSecond page"
    assert closed == [
        "First page",
        "page: First page",
        "Second page",
        "page: Second page",
        "document",
    ]


def test_pdf_text_quality_detects_pages_needing_ocr():
    assert rd._pdf_text_needs_ocr("")
    assert rd._pdf_text_needs_ocr("word" * 30)
    assert not rd._pdf_text_needs_ocr("This is a normal sentence with enough native PDF text.")


def test_ocr_page_falls_back_from_lighton_to_rapidocr(monkeypatch):
    class Bitmap:
        def to_pil(self):
            return types.SimpleNamespace(copy=lambda: "page image")

        def close(self):
            pass

    page = types.SimpleNamespace(render=lambda scale: Bitmap())
    calls = []

    def lighton():
        calls.append("load lighton")

        def fail(image):
            calls.append(("lighton", image))
            raise RuntimeError("model unavailable")

        return fail

    def rapidocr():
        calls.append("load rapidocr")
        return lambda image: calls.append(("rapidocr", image)) or "OCR text"

    monkeypatch.setattr(rd, "_OCR_READERS", {"lighton": lighton, "rapidocr": rapidocr})

    with pytest.warns(RuntimeWarning, match="lighton OCR failed"):
        text = rd._ocr_page(page, ("lighton", "rapidocr"), {}, set())

    assert text == "OCR text"
    assert calls == [
        "load lighton",
        ("lighton", "page image"),
        "load rapidocr",
        ("rapidocr", "page image"),
    ]


def test_ocr_page_does_not_render_without_an_installed_backend(monkeypatch):
    def unavailable():
        raise ModuleNotFoundError

    monkeypatch.setattr(rd, "_OCR_READERS", {"lighton": unavailable, "rapidocr": unavailable})
    page = types.SimpleNamespace(render=lambda scale: pytest.fail("page should not be rendered"))

    with pytest.warns(RuntimeWarning, match="no OCR backend was available"):
        assert rd._ocr_page(page, ("lighton", "rapidocr"), {}, set()) == ""
