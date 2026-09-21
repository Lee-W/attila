from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from pelican.generators import ArticlesGenerator

from tests.conftest import CONTENT_DIR, OUTPUT_DIR

if TYPE_CHECKING:
    from pelican.settings import Settings


def _template_generator(settings: Settings) -> ArticlesGenerator:
    context = settings.copy()
    context["generated_content"] = {}
    context["static_links"] = set()
    context["static_content"] = {}
    context["localsiteurl"] = settings["SITEURL"]
    return ArticlesGenerator(
        context=context,
        settings=settings,
        path=CONTENT_DIR,
        theme=settings["THEME"],
        output_path=OUTPUT_DIR,
    )


def _render_random_article(settings: Settings) -> BeautifulSoup:
    generator = _template_generator(settings)
    template = generator.env.from_string(
        '{% import "partials/i18n.html" as i18n with context %}'
        '{% include "partials/random_article.html" %}'
    )
    return BeautifulSoup(
        template.render(settings | {"page_lang": "en", "SITEURL": ""}),
        "html.parser",
    )


def test_random_article_button_renders_without_plugin_in_plugins_list(
    default_settings: Settings,
):
    # Regression test: the guard must not depend on a literal
    # "pelican.plugins.random_article" entry in PLUGINS. Sites can supply an
    # equivalent /random/ page through their own custom generator/plugin, and
    # the button should still show up as long as RANDOM_ARTICLE_BUTTON is on.
    default_settings["RANDOM_ARTICLE_BUTTON"] = True
    assert "pelican.plugins.random_article" not in default_settings["PLUGINS"]

    soup = _render_random_article(default_settings)

    aside = soup.select_one("aside.post-random")
    assert aside is not None
    link = aside.select_one("a")
    assert link is not None
    assert link["href"] == "/random/"
    assert "Read a random article" in link.get_text()


def test_random_article_button_hidden_when_setting_unset(default_settings: Settings):
    soup = _render_random_article(default_settings)
    assert soup.select_one("aside.post-random") is None


def test_random_article_button_hidden_when_setting_false(default_settings: Settings):
    default_settings["RANDOM_ARTICLE_BUTTON"] = False
    soup = _render_random_article(default_settings)
    assert soup.select_one("aside.post-random") is None


def test_random_article_button_link_follows_save_as(default_settings: Settings):
    default_settings["RANDOM_ARTICLE_BUTTON"] = True
    default_settings["RANDOM_ARTICLE_SAVE_AS"] = "custom-random/index.html"

    soup = _render_random_article(default_settings)

    link = soup.select_one("aside.post-random a")
    assert link is not None
    assert link["href"] == "/custom-random/"
