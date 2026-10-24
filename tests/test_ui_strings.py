"""UI strings and listing-page titles go through i18n.t instead of being English-only."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pelican.settings import Settings


def _zh(settings: Settings) -> Settings:
    settings["DEFAULT_LANG"] = "zh-tw"
    settings["SITE_LOGO"] = "/logo.png"
    return settings


class TestEnglishIsUnchanged:
    def test_listing_titles(
        self,
        default_settings: Settings,
        gen_category_and_html_from_name: Callable,
        gen_tag_and_html_from_name: Callable,
        gen_author_and_html_from_name: Callable,
    ):
        _, category = gen_category_and_html_from_name("foo", settings=default_settings)
        _, tag = gen_tag_and_html_from_name("footag", settings=default_settings)
        _, author = gen_author_and_html_from_name("arul", settings=default_settings)

        assert category.title.string == "Attila Demo - Articles in the foo category"
        assert tag.title.string == "Attila Demo - Tag footag"
        assert author.title.string == "Attila Demo - Articles by arul"

    def test_navigation_labels(
        self, default_settings: Settings, gen_index_and_html: Callable
    ):
        default_settings["SITE_LOGO"] = "/logo.png"
        soup = gen_index_and_html(settings=default_settings)

        assert soup.select_one(".nav-menu span").get_text() == "Menu"
        assert soup.select_one(".nav-close")["aria-label"] == "Close menu"
        assert soup.select_one(".logo a")["title"] == "Home"
        assert soup.select_one(".logo img")["alt"] == "Blog Logo"


class TestListingTitlesFollowThePageLanguage:
    def test_category_title_is_translated_and_uses_category_translations(
        self,
        default_settings: Settings,
        gen_category_and_html_from_name: Callable,
    ):
        settings = _zh(default_settings)
        settings["CATEGORY_TRANSLATIONS"] = {"foo": "福"}

        _, soup = gen_category_and_html_from_name("foo", settings=settings)

        assert soup.title.string == "Attila Demo - 福 分類的文章"

    def test_tag_title_is_translated(
        self,
        default_settings: Settings,
        gen_tag_and_html_from_name: Callable,
    ):
        _, soup = gen_tag_and_html_from_name("footag", settings=_zh(default_settings))

        assert soup.title.string == "Attila Demo - 標籤：footag"

    def test_author_title_is_translated(
        self,
        default_settings: Settings,
        gen_author_and_html_from_name: Callable,
    ):
        _, soup = gen_author_and_html_from_name("arul", settings=_zh(default_settings))

        assert soup.title.string == "Attila Demo - arul 的文章"

    def test_tag_cloud_tooltip_counts_posts_in_the_page_language(
        self,
        default_settings: Settings,
        render_direct_template: Callable,
    ):
        soup = render_direct_template("tags", settings=_zh(default_settings))

        tooltips = [a["title"] for a in soup.select(".tag-cloud a")]
        assert tooltips
        assert all(t.endswith("篇文章") for t in tooltips), tooltips


class TestChromeFollowsThePageLanguage:
    def test_navigation_labels(
        self, default_settings: Settings, gen_index_and_html: Callable
    ):
        soup = gen_index_and_html(settings=_zh(default_settings))

        assert soup.select_one(".nav-menu span").get_text() == "選單"
        assert soup.select_one(".nav-close")["aria-label"] == "關閉選單"
        assert soup.select_one(".logo a")["title"] == "首頁"
        assert soup.select_one(".logo img")["alt"] == "網站標誌"

    def test_comment_toggle_and_copy_button_are_translated(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        default_settings["SITEURL"] = "https://example.com"  # comments need a SITEURL
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=_zh(default_settings),
        )

        assert soup.select_one("#show-comments").get_text(strip=True) == "顯示留言"
        scripts = "".join(script.get_text() for script in soup.find_all("script"))
        # Emitted with |tojson, so decode the object literal instead of grepping.
        labels = json.loads(re.search(r"const labels = (\{.*?\});", scripts).group(1))
        assert labels == {"copy": "複製", "copied": "已複製", "failed": "複製失敗"}
