from __future__ import annotations

import json
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from bs4 import BeautifulSoup
    from pelican.settings import Settings


def _jsonld(soup: BeautifulSoup, type_: str) -> dict:
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        data = json.loads(script.string)
        if data.get("@type") == type_:
            return data
    raise AssertionError(f"no {type_} JSON-LD block found")


def test_article_published_time_is_iso_8601(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_with_og_image.rst",
        settings=default_settings,
    )

    published = soup.find("meta", attrs={"property": "article:published_time"})
    # str(datetime) uses a space separator, which Open Graph parsers reject.
    assert published["content"] == "2018-04-29T00:59:00+05:30"


def test_site_json_ld_uses_the_schema_org_website_type(
    default_settings: Settings,
    gen_index_and_html: Callable,
):
    soup = gen_index_and_html(settings=default_settings)

    assert _jsonld(soup, "WebSite")["name"] == default_settings["SITENAME"]


def test_site_json_ld_image_keeps_an_absolute_header_cover(
    default_settings: Settings,
    gen_index_and_html: Callable,
):
    default_settings["HEADER_COVER"] = "https://cdn.example.net/cover.jpg"

    soup = gen_index_and_html(settings=default_settings)

    # Prefixing the site URL would produce ".../https://cdn.example.net/...".
    assert _jsonld(soup, "WebSite")["image"] == "https://cdn.example.net/cover.jpg"


def test_site_json_ld_image_prefixes_a_relative_header_cover_once(
    default_settings: Settings,
    gen_index_and_html: Callable,
):
    default_settings["SITEURL"] = "https://example.com"
    default_settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"

    soup = gen_index_and_html(settings=default_settings)

    assert (
        _jsonld(soup, "WebSite")["image"]
        == "https://example.com/assets/images/header_cover.jpg"
    )


def test_article_json_ld_author_follows_author_meta_name(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    default_settings["AUTHOR_META"] = {"arul": {"name": "Arul Raj"}}

    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_special.rst",
        settings=default_settings,
    )

    assert _jsonld(soup, "Article")["author"]["name"] == "Arul Raj"
