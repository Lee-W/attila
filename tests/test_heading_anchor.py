from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from bs4 import BeautifulSoup
    from pelican.settings import Settings


def _anchor_script(soup: BeautifulSoup) -> str:
    scripts = [
        s.get_text() for s in soup.find_all("script") if "heading-anchor" in s.get_text()
    ]
    assert len(scripts) == 1
    return scripts[0]


def _label(script: str) -> str:
    # The label is emitted with |tojson, so non-ASCII text arrives as a backslash-u escape.
    match = re.search(r'setAttribute\("aria-label", ("(?:[^"\\]|\\.)*")', script)
    assert match is not None
    return json.loads(match.group(1))


def test_heading_anchor_is_named_instead_of_hidden(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    # The anchor is a real link that keyboards can focus, so hiding it from
    # assistive technology with aria-hidden contradicts its focusability.
    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_with_og_image.rst",
        settings=default_settings,
    )
    script = _anchor_script(soup)

    assert "aria-hidden" not in script
    assert 'setAttribute("aria-label"' in script
    assert _label(script) == "Link to this section"


def test_heading_anchor_label_is_translated(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_with_mixed_language_body.rst",
        settings=default_settings,
    )

    assert _label(_anchor_script(soup)) == "連結到此段落"
