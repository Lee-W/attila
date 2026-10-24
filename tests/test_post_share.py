from __future__ import annotations

from typing import TYPE_CHECKING, Callable
from urllib.parse import parse_qs, urlsplit

if TYPE_CHECKING:
    from pelican.settings import Settings


def _share_query(soup, css_class: str) -> dict[str, list[str]]:
    link = soup.select_one(f".post-share a.{css_class}")
    assert link is not None, css_class
    return parse_qs(urlsplit(link["href"]).query)


def test_share_links_url_encode_the_title_and_url(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    # The title contains `"`, `&` and spaces; unencoded, the `&` would end the
    # query parameter and the rest of the title would be read as a new one.
    default_settings["SITEURL"] = "https://example.com"
    article, soup = gen_article_and_html_from_rst(
        rst_path="content/article_special.rst",
        settings=default_settings,
    )
    title = 'Quote "He said" & more'
    article_url = f"https://example.com/{article.url}"

    assert _share_query(soup, "twitter") == {"text": [title], "url": [article_url]}
    assert _share_query(soup, "facebook") == {"u": [article_url]}
    assert _share_query(soup, "linkedin") == {
        "mini": ["true"],
        "url": [article_url],
        "title": [title],
    }
    assert _share_query(soup, "email") == {
        "subject": [title],
        "body": [article_url],
    }
