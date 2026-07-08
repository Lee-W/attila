from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from pelican.generators import ArticlesGenerator

from tests.conftest import CONTENT_DIR, OUTPUT_DIR

if TYPE_CHECKING:
    from pelican.settings import Settings


def _series_articles():
    first = SimpleNamespace(title="Part One", subtitle=None, url="2026/07/part-one.html")
    second = SimpleNamespace(
        title="Part Two",
        subtitle="The Return",
        url="2026/07/part-two.html",
    )
    series = SimpleNamespace(name="Deep Dive", all=[first, second])
    first.series = SimpleNamespace(name=series.name, index=1, all=series.all)
    second.series = SimpleNamespace(name=series.name, index=2, all=series.all)
    return first, second


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


def test_series_partial_renders_navigation(default_settings: Settings):
    first, second = _series_articles()
    generator = _template_generator(default_settings)
    template = generator.env.from_string(
        '{% import "partials/i18n.html" as i18n with context %}'
        '{% include "partials/series.html" %}'
    )
    soup = BeautifulSoup(
        template.render(
            default_settings | {"article": second, "page_lang": "en", "SITEURL": ""}
        ),
        "html.parser",
    )

    series = soup.select_one(".series")
    assert series is not None
    assert series.select_one("p").get_text(strip=True) == (
        'This post is part 2 of the "Deep Dive" series:'
    )
    assert [item.get_text(" ", strip=True) for item in series.select("ol.parts li")] == [
        "Part One",
        "Part Two - The Return",
    ]
    assert series.select_one("li.active a")["href"] == "/2026/07/part-two.html"


def test_series_partial_uses_zh_tw_workaround(default_settings: Settings):
    _, second = _series_articles()
    generator = _template_generator(default_settings)
    template = generator.env.from_string(
        '{% import "partials/i18n.html" as i18n with context %}'
        '{% include "partials/series.html" %}'
    )
    soup = BeautifulSoup(
        template.render(
            default_settings | {"article": second, "page_lang": "zh-tw", "SITEURL": ""}
        ),
        "html.parser",
    )

    assert soup.select_one(".series p").get_text(strip=True) == (
        "本文是「Deep Dive」系列的第 2 篇："
    )


def test_series_list_builds_index_from_articles(default_settings: Settings):
    first, second = _series_articles()
    generator = _template_generator(default_settings)
    soup = BeautifulSoup(
        generator.get_template("series_list").render(
            generator.context | {"articles": [second, first]}
        ),
        "html.parser",
    )

    item = soup.select_one(".series-index-item")
    assert item is not None
    assert item.select_one(".series-index-link")["href"] == "/2026/07/part-one.html"
    assert item.select_one(".series-index-name").get_text(strip=True) == "Deep Dive"
    assert item.select_one(".series-index-count").get_text(strip=True) == "2"
