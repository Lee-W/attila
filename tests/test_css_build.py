from __future__ import annotations

import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS_SRC = REPO_ROOT / "css-src"
STYLE_CSS = REPO_ROOT / "src/pelican/themes/attila/static/css/style.css"


def test_style_css_matches_sources():
    """The shipped style.css must equal the concatenation of css-src/*.css.

    Edit the modules in css-src/ and run `uv run poe build-css`; the generated
    style.css is never edited directly. This test guards against drift.
    """
    parts = sorted(CSS_SRC.glob("*.css"))
    assert parts, "no css-src/*.css modules found"
    rebuilt = "".join(part.read_text() for part in parts)
    assert STYLE_CSS.read_text() == rebuilt, (
        "style.css is out of sync with css-src/. Run `uv run poe build-css`."
    )
