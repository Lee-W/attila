from __future__ import annotations

import json
from typing import TYPE_CHECKING, Callable

import pytest

if TYPE_CHECKING:
    from bs4 import BeautifulSoup
    from pelican.settings import Settings


def _article_jsonld(soup: BeautifulSoup) -> dict:
    """Return the parsed Article JSON-LD, asserting every block is valid JSON."""
    for script in soup.find_all(name="script", attrs={"type": "application/ld+json"}):
        data = json.loads(script.string)  # raises on malformed JSON
        if data.get("@type") == "Article":
            return data
    raise AssertionError("no Article JSON-LD block found")


class TestHtmlLang:
    def test_html_lang_follows_article(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        # DEFAULT_LANG is "en"; this article declares :lang: fr, so the
        # document language must be "fr", not the site default.
        result, soup = gen_article_and_html_from_rst(
            rst_path="content/article_special.rst",
            settings=default_settings,
        )
        assert result.lang == "fr"
        assert soup.find(name="html")["lang"] == "fr"


class TestJsonLd:
    def test_dates_are_iso_8601(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        data = _article_jsonld(soup)
        # ISO 8601 uses a "T" separator, e.g. 2018-04-29T00:45:00+05:30 —
        # the default datetime str ("2018-04-29 00:45:00") is rejected by
        # Google's structured-data parser.
        assert "T" in data["datePublished"]

    def test_survives_special_characters(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        # Quotes and ampersands in the title/summary must not break the JSON.
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_special.rst",
            settings=default_settings,
        )
        data = _article_jsonld(soup)  # json.loads would raise on bad escaping
        assert '"He said"' in data["name"]


class TestArticleMetadata:
    def test_content_pages_emit_one_description(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
        gen_page_and_html_from_rst: Callable,
    ):
        default_settings["SITE_DESCRIPTION"] = "Fallback site description"

        _, article_soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        _, page_soup = gen_page_and_html_from_rst(
            rst_path="content/pages/page_without_cover_image.rst",
            settings=default_settings,
        )

        assert len(article_soup.select('meta[name="description"]')) == 1
        assert len(page_soup.select('meta[name="description"]')) == 1

    def test_visible_dates_use_iso_datetime_values(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        published = soup.select_one(".post-head-date time")
        assert "T" in published["datetime"]

    def test_description_falls_back_to_site_description(
        self,
        default_settings: Settings,
        gen_page_and_html_from_rst: Callable,
    ):
        default_settings["SITE_DESCRIPTION"] = "Fallback site description"
        _, soup = gen_page_and_html_from_rst(
            rst_path="content/pages/page_without_cover_image.rst",
            settings=default_settings,
        )
        assert soup.select_one('meta[property="og:description"]')["content"] == (
            "Fallback site description"
        )

    def test_missing_author_avatar_does_not_emit_empty_image(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        assert not soup.select('img[src=""]')


class TestFooterCredits:
    def test_custom_left_and_right_both_render(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        default_settings["SHOW_CREDITS"] = {"left": "LEFTMARK", "right": "RIGHTMARK"}
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        credits = soup.find(name="span", attrs={"class": "nav-credits"}).get_text()
        assert "LEFTMARK" in credits
        assert "RIGHTMARK" in credits


class TestSkipLinkTargets:
    @pytest.mark.parametrize("name", ["tags", "authors", "categories", "archives"])
    def test_listing_pages_expose_site_main(
        self,
        render_direct_template: Callable,
        name: str,
    ):
        soup = render_direct_template(name)
        skip = soup.find(name="a", attrs={"class": "skip-link"})
        assert skip is not None
        assert skip["href"] == "#site-main"
        assert soup.find(name="main", attrs={"id": "site-main"}) is not None
