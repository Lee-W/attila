from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Callable

import pytest
from pelican import signals
from pelican.contents import Article

from pelican.themes.attila.readtime import add_readtime, count_text


def _make_article(content: str) -> Article:
    return Article(
        content=content,
        metadata={"title": "Readtime fixture", "date": datetime(2026, 7, 2)},
    )


def test_count_text_counts_cjk_characters_without_punctuation():
    assert count_text("<p>這是一段中文，含全形標點。</p>") == (11, 0)


def test_count_text_counts_latin_words():
    assert count_text("<p>Hello world, it's a mixed-language test 123.</p>") == (0, 7)


def test_count_text_counts_non_ascii_words():
    assert count_text("<p>élève déjà vu — Привет мир</p>") == (0, 5)


def test_count_text_counts_mixed_language_content():
    cjk, words = count_text("<p>我用 Pelican 寫部落格</p>")
    assert (cjk, words) == (6, 1)


def test_count_text_strips_tags_and_entities():
    assert count_text("<code>&lt;div&gt;</code> 標籤") == (2, 1)


def test_add_readtime_sets_minutes_and_word_count():
    article = _make_article("<p>" + "中" * 1150 + " word " * 50 + "</p>")
    add_readtime(article)
    # 1150 chars / 300 cpm + 50 words / 250 wpm = 4.03 → ceil to 5
    assert article.readtime == 5
    assert article.readtime_word_count == 1200


def test_add_readtime_rounds_short_content_up_to_one_minute():
    article = _make_article("<p>很短的一篇</p>")
    add_readtime(article)
    assert article.readtime == 1
    assert article.readtime_word_count == 5


def test_add_readtime_respects_speed_settings():
    article = _make_article("<p>" + "中" * 600 + "</p>")
    article.settings["READTIME_CJK_CPM"] = 100
    add_readtime(article)
    assert article.readtime == 6


@pytest.mark.parametrize("setting", [0, -1, "fast", float("inf")])
def test_add_readtime_rejects_invalid_speed_settings(setting):
    article = _make_article("<p>content</p>")
    article.settings["READTIME_WPM"] = setting
    with pytest.raises(ValueError, match="READTIME_WPM must be a positive number"):
        add_readtime(article)


def test_add_readtime_skips_empty_content():
    article = _make_article("")
    add_readtime(article)
    assert not hasattr(article, "readtime")


def test_add_readtime_ignores_non_content_objects():
    static = SimpleNamespace(_content="<p>plenty of words here</p>", settings={})
    add_readtime(static)
    assert not hasattr(static, "readtime")


def test_article_template_renders_readtime_meta(
    gen_article_and_html_from_rst: Callable,
):
    signals.content_object_init.connect(add_readtime)
    try:
        _, soup = gen_article_and_html_from_rst("content/article_special.rst")
    finally:
        signals.content_object_init.disconnect(add_readtime)
    meta = soup.select_one(".post-meta").get_text()
    assert "min read" in meta
    assert "words" in meta


def test_article_template_omits_readtime_when_plugin_is_disabled(
    gen_article_and_html_from_rst: Callable,
):
    _, soup = gen_article_and_html_from_rst("content/article_special.rst")
    meta = soup.select_one(".post-meta").get_text()
    assert "min read" not in meta
    assert "words" not in meta


def test_article_template_renders_readtime_meta_in_zh_tw(
    gen_article_and_html_from_rst: Callable,
):
    signals.content_object_init.connect(add_readtime)
    try:
        _, soup = gen_article_and_html_from_rst(
            "content/article_with_mixed_language_body.rst"
        )
    finally:
        signals.content_object_init.disconnect(add_readtime)
    meta = soup.select_one(".post-meta").get_text()
    assert "閱讀時間約 1 分鐘" in meta
    assert "共 34 字" in meta


def test_tag_listing_hides_readtime_by_default(
    gen_tag_and_html_from_name: Callable,
):
    signals.content_object_init.connect(add_readtime)
    try:
        _, soup = gen_tag_and_html_from_name("bartag")
    finally:
        signals.content_object_init.disconnect(add_readtime)
    assert not soup.select(".post-card-readtime")


def test_tag_listing_shows_readtime_when_enabled(
    gen_tag_and_html_from_name: Callable,
    default_settings,
):
    default_settings["SHOW_READTIME_IN_ARTICLE_SUMMARY"] = True
    signals.content_object_init.connect(add_readtime)
    try:
        _, soup = gen_tag_and_html_from_name("bartag")
    finally:
        signals.content_object_init.disconnect(add_readtime)
    cards = soup.select(".post-card-readtime")
    assert [card.get_text() for card in cards] == ["1 min read"]
