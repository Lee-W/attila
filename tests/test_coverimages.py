from __future__ import annotations

from typing import Callable

from pelican.settings import Settings


class TestArticleCoverImage:
    def test_article_cover(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        default_settings["SITEURL"] = "http://www.example.com"
        result, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_cover_image.rst",
        )
        selected = soup.find(name="div", attrs={"class": "post-cover cover"})
        assert selected is not None
        selected_img = selected.find(name="img")
        assert selected_img is not None
        assert f"{default_settings['SITEURL']}{result.cover}" in selected_img["src"]

    def test_article_header_cover(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        default_settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_without_cover.rst",
        )
        selected = soup.find(name="div", attrs={"class": "post-cover cover"})
        assert selected is not None
        selected_img = selected.find(name="img")
        assert selected_img is not None
        assert (
            f"{default_settings['SITEURL']}{default_settings['HEADER_COVER']}"
            in selected_img["src"]
        )

    def test_article_header_http_cover(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        default_settings["HEADER_COVER"] = "http://example.com/cover.jpg"

        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_without_cover.rst",
        )

        selected = soup.find(name="div", class_="post-cover cover")
        assert selected is not None

        selected_img = selected.find(name="img")
        assert selected_img is not None
        assert default_settings["HEADER_COVER"] in selected_img["src"]

    def test_article_theme_cover(
        self,
        gen_article_and_html_from_rst: Callable,
    ):
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_without_cover.rst"
        )

        selected = soup.find(name="div", class_="post-cover")
        assert selected is None

    def test_article_header_color(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        default_settings["HEADER_COLOR"] = "blue"

        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_without_cover.rst"
        )

        selected = soup.find(name="div", class_="post-cover cover")
        assert selected is not None
        assert default_settings["HEADER_COLOR"] in selected["style"]

    def test_article_http_cover(
        self,
        gen_article_and_html_from_rst: Callable,
    ):
        result, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_http_cover_image.rst"
        )

        selected = soup.find(name="div", class_="post-cover cover")
        assert selected is not None

        selected_img = selected.find(name="img")
        assert selected_img is not None
        assert result.cover in selected_img["src"]

    def test_article_og_cover(
        self,
        gen_article_and_html_from_rst: Callable,
    ):
        result, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst"
        )

        selected = soup.find(name="div", class_="post-cover cover")
        assert selected is not None

        selected_img = selected.find(name="img")
        assert selected_img is not None
        assert result.og_image in selected_img["src"]


class TestPageCoverImage:
    def test_page_cover(
        self,
        default_settings: Settings,
        gen_page_and_html_from_rst: Callable,
    ):
        default_settings["SITEURL"] = "http://www.example.com"

        result, soup = gen_page_and_html_from_rst(
            rst_path="content/pages/page_with_cover_image.rst"
        )

        selected = soup.find(name="div", attrs={"class": "post-cover cover"})
        selected_img = selected.find(name="img")

        assert f"{default_settings['SITEURL']}/{result.cover}" in selected_img["src"]

    def test_page_header_cover(
        self,
        default_settings: Settings,
        gen_page_and_html_from_rst: Callable,
    ):
        default_settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"

        result, soup = gen_page_and_html_from_rst(
            rst_path="content/pages/page_without_cover_image.rst"
        )

        selected = soup.find(name="div", attrs={"class": "post-cover cover"})
        selected_img = selected.find(name="img")

        assert (
            f"{default_settings['SITEURL']}{default_settings['HEADER_COVER']}"
            in selected_img["src"]
        )

    def test_page_header_http_cover(
        self,
        default_settings: Settings,
        gen_page_and_html_from_rst: Callable,
    ):
        default_settings["HEADER_COVER"] = "http://example.com/cover.jpg"

        result, soup = gen_page_and_html_from_rst(
            rst_path="content/pages/page_without_cover_image.rst"
        )

        selected = soup.find(name="div", attrs={"class": "post-cover cover"})
        selected_img = selected.find(name="img")

        assert default_settings["HEADER_COVER"] in selected_img["src"]

    def test_page_theme_cover(
        self,
        gen_page_and_html_from_rst: Callable,
    ):
        result, soup = gen_page_and_html_from_rst(
            rst_path="content/pages/page_without_cover_image.rst"
        )

        selected = soup.find(name="div", attrs={"class": "post-cover"})

        assert selected is None

    def test_page_header_color(
        self,
        default_settings: Settings,
        gen_page_and_html_from_rst: Callable,
    ):
        default_settings["HEADER_COLOR"] = "blue"

        result, soup = gen_page_and_html_from_rst(
            rst_path="content/pages/page_without_cover_image.rst"
        )

        selected = soup.find(name="div", attrs={"class": "post-cover cover"})

        assert default_settings["HEADER_COLOR"] in selected["style"]

    def test_page_http_cover(
        self,
        gen_page_and_html_from_rst: Callable,
    ):
        result, soup = gen_page_and_html_from_rst(
            rst_path="content/pages/page_with_http_cover_image.rst"
        )

        selected = soup.find(name="div", attrs={"class": "post-cover cover"})
        selected_img = selected.find(name="img")

        assert result.cover in selected_img["src"]

    def test_page_og_cover(
        self,
        gen_page_and_html_from_rst: Callable,
    ):
        result, soup = gen_page_and_html_from_rst(
            rst_path="content/pages/page_with_og_image.rst"
        )

        selected = soup.find(name="div", attrs={"class": "post-cover cover"})
        selected_img = selected.find(name="img")

        assert result.og_image in selected_img["src"]


class TestTagCoverImage:
    def test_footag_theme_cover(self, gen_tag_and_html_from_name):
        result, soup = gen_tag_and_html_from_name("footag")
        selected = soup.find(name="div", class_="post-cover")
        assert selected is None

    def test_footag_cover(self, default_settings: Settings, gen_tag_and_html_from_name):
        tag_name = "footag"
        default_settings["TAG_META"] = {
            tag_name: {"cover": "/assets/images/foo_tag_cover.jpg"}
        }
        result, soup = gen_tag_and_html_from_name(tag_name)
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert (
            f"{default_settings['SITEURL']}{default_settings['TAG_META'][tag_name]['cover']}"
            in selected_img["src"]
        )

    def test_footag_http_cover(
        self, default_settings: Settings, gen_tag_and_html_from_name
    ):
        tag_name = "footag"
        default_settings["TAG_META"] = {
            tag_name: {"cover": "http://examble.com/cover.jpg"}
        }
        result, soup = gen_tag_and_html_from_name(tag_name)
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert default_settings["TAG_META"][tag_name]["cover"] in selected_img["src"]

    def test_footag_header_cover(
        self, default_settings: Settings, gen_tag_and_html_from_name
    ):
        default_settings["SITEURL"] = "http://example.com"
        default_settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
        result, soup = gen_tag_and_html_from_name("footag")
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert (
            f"{default_settings['SITEURL']}{default_settings['HEADER_COVER']}"
            in selected_img["src"]
        )

    def test_footag_header_http_cover(
        self, default_settings: Settings, gen_tag_and_html_from_name
    ):
        default_settings["HEADER_COVER"] = "http://example.com/cover.jpg"
        result, soup = gen_tag_and_html_from_name("footag")
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert default_settings["HEADER_COVER"] in selected_img["src"]

    def test_footag_header_color(
        self, default_settings: Settings, gen_tag_and_html_from_name
    ):
        default_settings["HEADER_COLOR"] = "red"
        result, soup = gen_tag_and_html_from_name("footag")
        selected = soup.find(name="div", class_="blog-cover cover")
        assert default_settings["HEADER_COLOR"] in selected["style"]

    def test_bartag_theme_cover(self, gen_tag_and_html_from_name):
        result, soup = gen_tag_and_html_from_name("bartag")
        selected = soup.find(name="div", class_="post-cover")
        assert selected is None

    def test_bartag_cover(self, default_settings: Settings, gen_tag_and_html_from_name):
        tag_name = "bartag"
        default_settings["TAG_META"] = {
            tag_name: {"cover": "/assets/images/bar_tag_cover.jpg"}
        }
        result, soup = gen_tag_and_html_from_name(tag_name)
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert (
            f"{default_settings['SITEURL']}{default_settings['TAG_META'][tag_name]['cover']}"
            in selected_img["src"]
        )

    def test_bartag_http_cover(
        self, default_settings: Settings, gen_tag_and_html_from_name
    ):
        tag_name = "bartag"
        default_settings["TAG_META"] = {
            tag_name: {"cover": "http://examble.com/cover.jpg"}
        }
        result, soup = gen_tag_and_html_from_name(tag_name)
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert default_settings["TAG_META"][tag_name]["cover"] in selected_img["src"]

    def test_bartag_header_cover(
        self, default_settings: Settings, gen_tag_and_html_from_name
    ):
        default_settings["SITEURL"] = "http://example.com"
        default_settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
        result, soup = gen_tag_and_html_from_name("bartag")
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert (
            f"{default_settings['SITEURL']}{default_settings['HEADER_COVER']}"
            in selected_img["src"]
        )

    def test_bartag_header_http_cover(
        self, default_settings: Settings, gen_tag_and_html_from_name
    ):
        default_settings["HEADER_COVER"] = "http://example.com/cover.jpg"
        result, soup = gen_tag_and_html_from_name("bartag")
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert default_settings["HEADER_COVER"] in selected_img["src"]

    def test_bartag_header_color(
        self, default_settings: Settings, gen_tag_and_html_from_name
    ):
        default_settings["HEADER_COLOR"] = "red"
        result, soup = gen_tag_and_html_from_name("bartag")
        selected = soup.find(name="div", class_="blog-cover cover")
        assert default_settings["HEADER_COLOR"] in selected["style"]


class TestCategoryCoverImage:
    def test_foo_theme_cover(self, gen_category_and_html_from_name):
        category, soup = gen_category_and_html_from_name("foo")
        selected = soup.find(name="div", class_="post-cover")
        assert selected is None

    def test_foo_cover(
        self, default_settings: Settings, gen_category_and_html_from_name
    ):
        category_name = "foo"
        default_settings["CATEGORY_META"] = {
            category_name: {"cover": "/assets/images/foo_category_cover.jpg"}
        }
        category, soup = gen_category_and_html_from_name(category_name)
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert (
            f"{default_settings['SITEURL']}{default_settings['CATEGORY_META'][category_name]['cover']}"
            in selected_img["src"]
        )

    def test_foo_http_cover(
        self, default_settings: Settings, gen_category_and_html_from_name
    ):
        category_name = "foo"
        default_settings["CATEGORY_META"] = {
            category_name: {"cover": "http://examble.com/cover.jpg"}
        }
        category, soup = gen_category_and_html_from_name(category_name)
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert (
            default_settings["CATEGORY_META"][category_name]["cover"]
            in selected_img["src"]
        )

    def test_foo_header_cover(
        self, default_settings: Settings, gen_category_and_html_from_name
    ):
        default_settings["SITEURL"] = "http://example.com"
        default_settings["HEADER_COVER"] = "/assets/images/header_cover.jpg"
        category, soup = gen_category_and_html_from_name("foo")
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert (
            f"{default_settings['SITEURL']}{default_settings['HEADER_COVER']}"
            in selected_img["src"]
        )

    def test_foo_header_http_cover(
        self, default_settings: Settings, gen_category_and_html_from_name
    ):
        default_settings["HEADER_COVER"] = "http://example.com/cover.jpg"
        category, soup = gen_category_and_html_from_name("foo")
        selected = soup.find(name="div", class_="blog-cover cover")
        selected_img = selected.find(name="img")
        assert default_settings["HEADER_COVER"] in selected_img["src"]

    def test_foo_header_color(
        self, default_settings: Settings, gen_category_and_html_from_name
    ):
        default_settings["HEADER_COLOR"] = "red"
        category, soup = gen_category_and_html_from_name("foo")
        selected = soup.find(name="div", class_="blog-cover cover")
        assert default_settings["HEADER_COLOR"] in selected["style"]

    def test_bar_theme_cover(self, gen_category_and_html_from_name):
        category, soup = gen_category_and_html_from_name("bar")
        selected = soup.find(name="div", class_="post-cover")
        assert selected is None
