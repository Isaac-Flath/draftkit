import sys
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
    url2md = lambda url, sel: (url, sel)
    monkeypatch.setitem(sys.modules, "playwrightnb", types.SimpleNamespace(url2md=url2md))

    assert rd.read_link("https://example.org", heavy=True) == (
        "https://example.org",
        "body",
    )
