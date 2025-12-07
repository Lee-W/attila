from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pelican.settings import Settings

logger = logging.getLogger(__name__)


class TestAuthorSocialLinks:
    def test_linkedin_link(
        self,
        default_settings: Settings,
        gen_article_and_html_from_rst: Callable,
        gen_author_and_html_from_name: Callable,
    ):
        author_name = "raj"
        default_settings.update(
            AUTHOR_META={
                author_name: {
                    "cover": "http://examble.com/cover.jpg",
                    "linkedin": "mylinkedinname",
                }
            },
            SHOW_AUTHOR_BIO_IN_ARTICLE=True,
        )

        _, soup = gen_article_and_html_from_rst(
            rst_path="content/article_with_og_image.rst",
            settings=default_settings,
        )
        selected = soup.find(name="span", attrs={"class": "post-author-linkedin"})
        assert selected is not None
        selected_anchor = selected.find(name="a")
        assert selected_anchor is not None
        assert "https://www.linkedin.com/in/mylinkedinname" in selected_anchor["href"]

        _, soup = gen_author_and_html_from_name(
            name=author_name, settings=default_settings
        )
        selected = soup.find(name="span", attrs={"class": "archive-links"})
        assert selected is not None
        assert "https://www.linkedin.com/in/mylinkedinname" in str(selected)
