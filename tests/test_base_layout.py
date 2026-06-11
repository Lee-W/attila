from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pelican.settings import Settings

logger = logging.getLogger(__name__)


class TestBaseLayout:
    def test_skip_link_targets_main(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        skip_link = soup.find(name="a", attrs={"class": "skip-link"})
        assert skip_link is not None
        assert skip_link["href"] == "#site-main"

        main = soup.find(name="main", attrs={"id": "site-main"})
        assert main is not None

    def test_theme_applied_before_first_paint(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        head = soup.find(name="head")
        inline_scripts = [s for s in head.find_all(name="script") if not s.get("src")]
        assert any("attila_theme" in (s.string or "") for s in inline_scripts), (
            "head must contain the inline theme-restore script to avoid FOUC"
        )

    def test_no_client_side_highlighter(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        scripts = soup.find_all(name="script", attrs={"src": True})
        assert not any("highlight" in s["src"] for s in scripts), (
            "highlighting happens at build time via Pygments; "
            "no client-side highlighter should be loaded"
        )

    def test_footer_renders_with_extra_hook(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
    ):
        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        nav_footer = soup.find(name="div", attrs={"class": "nav-footer"})
        assert nav_footer is not None
