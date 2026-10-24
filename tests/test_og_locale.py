from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from bs4 import BeautifulSoup
    from pelican.settings import Settings


def _og_locale(soup: BeautifulSoup) -> str:
    return soup.find("meta", attrs={"property": "og:locale"})["content"]


def test_article_locale_follows_its_language_over_the_site_setting(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    default_settings["OG_LOCALE"] = "en_GB"

    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_with_mixed_language_body.rst",  # :lang: zh-tw
        settings=default_settings,
    )

    assert _og_locale(soup) == "zh_TW"


def test_default_language_keeps_the_configured_locale(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    default_settings["OG_LOCALE"] = "en_GB"

    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_with_og_image.rst",
        settings=default_settings,
    )

    assert _og_locale(soup) == "en_GB"


def test_unmapped_language_falls_back_to_the_configured_locale(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    default_settings["OG_LOCALE"] = "en_GB"

    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_special.rst",  # :lang: fr
        settings=default_settings,
    )

    assert _og_locale(soup) == "en_GB"


def test_listing_page_locale_follows_the_site_language(
    default_settings: Settings,
    gen_index_and_html: Callable,
):
    default_settings["DEFAULT_LANG"] = "ja"

    soup = gen_index_and_html(settings=default_settings)

    assert _og_locale(soup) == "ja_JP"


def test_front_matter_og_locale_still_wins(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    # article_with_mixed_language_body is zh-tw; nothing sets og_locale there,
    # so reuse the setting-vs-language rule: the explicit key must beat both.
    default_settings["OG_LOCALE"] = "en_GB"
    default_settings["DEFAULT_METADATA"] = {"og_locale": "zh_HK"}

    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_with_mixed_language_body.rst",
        settings=default_settings,
    )

    assert _og_locale(soup) == "zh_HK"
