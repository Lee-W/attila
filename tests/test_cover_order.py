from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pelican.settings import Settings


def test_page_color_beats_the_site_wide_cover(
    default_settings: Settings,
    gen_page_and_html_from_rst: Callable,
):
    # Articles already rank their own `color:` above HEADER_COVER, so a page
    # that sets a colour must not be overridden by the site-wide cover either.
    default_settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    default_settings["HOME_COVER"] = "/assets/images/home_cover.jpg"

    _, soup = gen_page_and_html_from_rst(
        rst_path="content/pages/page_with_color.rst",
        settings=default_settings,
    )

    cover = soup.select_one(".post-cover")
    assert cover is not None
    assert cover.select_one("img") is None
    assert "background-color: #123456" in cover["style"]


def test_page_falls_back_to_home_cover_when_nothing_else_is_set(
    default_settings: Settings,
    gen_page_and_html_from_rst: Callable,
):
    default_settings["HOME_COVER"] = "/assets/images/home_cover.jpg"

    _, soup = gen_page_and_html_from_rst(
        rst_path="content/pages/page_without_cover_image.rst",
        settings=default_settings,
    )

    assert soup.select_one(".post-cover img")["src"].endswith(
        "/assets/images/home_cover.jpg"
    )


def test_article_falls_back_to_home_cover_and_og_image(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    default_settings["HOME_COVER"] = "/assets/images/home_cover.jpg"

    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_without_cover.rst",
    )

    assert soup.select_one(".post-cover img")["src"].endswith(
        "/assets/images/home_cover.jpg"
    )
    og_image = soup.select_one('meta[property="og:image"]')
    assert og_image["content"].endswith("/assets/images/home_cover.jpg")


def test_header_cover_beats_home_cover(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    default_settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
    default_settings["HOME_COVER"] = "/assets/images/home_cover.jpg"

    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_without_cover.rst",
    )

    assert soup.select_one(".post-cover img")["src"].endswith(
        "/assets/images/header_cover.jpg"
    )


def test_tag_page_falls_back_to_home_color(
    default_settings: Settings,
    gen_tag_and_html_from_name: Callable,
):
    default_settings["HOME_COLOR"] = "#abcdef"

    _, soup = gen_tag_and_html_from_name("footag")

    cover = soup.select_one(".blog-cover")
    assert cover is not None
    assert cover.select_one("img") is None
    assert "background-color: #abcdef" in cover["style"]


def test_category_page_falls_back_to_home_color(
    default_settings: Settings,
    gen_category_and_html_from_name: Callable,
):
    default_settings["HOME_COLOR"] = "#abcdef"

    _, soup = gen_category_and_html_from_name("foo")

    cover = soup.select_one(".blog-cover")
    assert cover is not None
    assert "background-color: #abcdef" in cover["style"]
