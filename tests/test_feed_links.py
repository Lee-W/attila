from __future__ import annotations

import functools
import itertools
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Callable

import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

if TYPE_CHECKING:
    from pelican.settings import Settings

TEMPLATE_DIR = (
    Path(__file__).parent.parent / "src" / "pelican" / "themes" / "attila" / "templates"
)

# partials/feed.html as shipped in 3.4.1. With FEED_LINK_TITLES and
# FEED_EXTRA_LINKS unset, the current partial must render the same bytes.
LEGACY_FEED_TEMPLATE = """\
{% set global_feeds = [
  ("atom", FEED_ALL_ATOM),
  ("rss", FEED_ALL_RSS),
  ("atom", FEED_ATOM),
  ("rss", FEED_RSS)
] %}

{% for fmt, feed in global_feeds if feed %}
<link href="{{ FEED_DOMAIN }}/{{ feed }}" type="application/{{ fmt }}+xml"
      rel="alternate" title="{{ SITENAME }} Full {{ fmt|upper }} Feed" />
{% endfor %}

{% set entity_feeds = [
  ("category", CATEGORY_FEED_ATOM, CATEGORY_FEED_RSS, category),
  ("tag", TAG_FEED_ATOM, TAG_FEED_RSS, tag),
  ("author", AUTHOR_FEED_ATOM, AUTHOR_FEED_RSS, author)
] %}

{% for entity_name, atom_feed, rss_feed, entity in entity_feeds if entity %}
  {% if atom_feed %}
  <link href="{{ FEED_DOMAIN }}/{{ atom_feed.format(slug=entity.slug) }}" type="application/atom+xml"
        rel="alternate" title="{{ SITENAME }} {{ entity_name|capitalize }} Atom Feed" />
  {% endif %}

  {% if rss_feed %}
  <link href="{{ FEED_DOMAIN }}/{{ rss_feed.format(slug=entity.slug) }}" type="application/rss+xml"
        rel="alternate" title="{{ SITENAME }} {{ entity_name|capitalize }} RSS Feed" />
  {% endif %}
{% endfor %}
"""

FEED_SETTINGS = {
    "FEED_ALL_ATOM": "feeds/all.atom.xml",
    "FEED_ALL_RSS": "feeds/all.rss.xml",
    "FEED_ATOM": "feeds/en.atom.xml",
    "FEED_RSS": "feeds/en.rss.xml",
    "CATEGORY_FEED_ATOM": "feeds/{slug}.atom.xml",
    "CATEGORY_FEED_RSS": "feeds/{slug}.rss.xml",
    "TAG_FEED_ATOM": "feeds/tag-{slug}.atom.xml",
    "TAG_FEED_RSS": "feeds/tag-{slug}.rss.xml",
    "AUTHOR_FEED_ATOM": "feeds/author-{slug}.atom.xml",
    "AUTHOR_FEED_RSS": "feeds/author-{slug}.rss.xml",
}
ENTITIES = {
    "category": SimpleNamespace(name="Food", slug="food"),
    "tag": SimpleNamespace(name="Tokyo", slug="tokyo"),
    "author": SimpleNamespace(name="Jane", slug="jane"),
}


@functools.cache
def _environment(trim: bool) -> Environment:
    # Pelican's default JINJA_ENVIRONMENT trims blocks, but a site that sets
    # its own JINJA_ENVIRONMENT (e.g. only to add extensions) does not.
    return Environment(
        loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=trim, lstrip_blocks=trim
    )


def _render(context: dict, trim: bool = True) -> str:
    return _environment(trim).get_template("partials/feed.html").render(context)


def _links(html: str) -> list[tuple[str, str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    return [
        (link["href"], link["type"], link["title"])
        for link in soup.find_all("link", rel="alternate")
    ]


def _contexts():
    """Every on/off combination of the feed settings and page entities."""
    for feeds_on in itertools.product((False, True), repeat=len(FEED_SETTINGS)):
        for entities_on in itertools.product((False, True), repeat=len(ENTITIES)):
            context = {
                "SITENAME": "Tom & Jerry",
                "FEED_DOMAIN": "https://example.com",
                "CATEGORY_TRANSLATIONS": {"Food": "Eats"},
            }
            for (name, value), on in zip(FEED_SETTINGS.items(), feeds_on):
                context[name] = value if on else None
            for (name, value), on in zip(ENTITIES.items(), entities_on):
                if on:
                    context[name] = value
            yield context


@pytest.mark.parametrize("trim", [True, False])
def test_unset_settings_render_the_legacy_html(trim: bool):
    legacy = _environment(trim).from_string(LEGACY_FEED_TEMPLATE)
    for context in _contexts():
        assert _render(context, trim) == legacy.render(context)


def test_link_titles_override_each_feed_and_format_entity_names():
    context = {
        "SITENAME": "Site",
        "FEED_DOMAIN": "https://example.com",
        **FEED_SETTINGS,
        **ENTITIES,
        "CATEGORY_TRANSLATIONS": {"Food": "Eats"},
        "FEED_LINK_TITLES": {
            "FEED_ATOM": 'Site "English"',
            "CATEGORY_FEED_ATOM": "Site: {name}",
            "TAG_FEED_RSS": "Tag {name}",
            "AUTHOR_FEED_ATOM": "By {name}",
        },
    }
    titles = {href: title for href, _, title in _links(_render(context))}

    assert titles["https://example.com/feeds/en.atom.xml"] == 'Site "English"'
    # The category name goes through CATEGORY_TRANSLATIONS like on the page.
    assert titles["https://example.com/feeds/food.atom.xml"] == "Site: Eats"
    assert titles["https://example.com/feeds/tag-tokyo.rss.xml"] == "Tag Tokyo"
    assert titles["https://example.com/feeds/author-jane.atom.xml"] == "By Jane"
    # Feeds without an entry keep the default title.
    assert titles["https://example.com/feeds/all.atom.xml"] == "Site Full ATOM Feed"
    assert titles["https://example.com/feeds/food.rss.xml"] == "Site Category RSS Feed"


def test_extra_links_are_listed_after_the_site_feeds_with_their_own_href():
    context = {
        "SITENAME": "Site",
        "FEED_DOMAIN": "https://example.com/ja",
        "FEED_ATOM": "feeds/all.atom.xml",
        "CATEGORY_FEED_ATOM": "feeds/{slug}.atom.xml",
        "category": ENTITIES["category"],
        "FEED_EXTRA_LINKS": (
            ("All languages", "https://example.com/feeds/all.atom.xml"),
            ("Podcast", "/podcast.rss", "rss"),
        ),
    }

    assert _links(_render(context)) == [
        (
            "https://example.com/ja/feeds/all.atom.xml",
            "application/atom+xml",
            "Site Full ATOM Feed",
        ),
        (
            "https://example.com/feeds/all.atom.xml",
            "application/atom+xml",
            "All languages",
        ),
        ("/podcast.rss", "application/rss+xml", "Podcast"),
        (
            "https://example.com/ja/feeds/food.atom.xml",
            "application/atom+xml",
            "Site Category Atom Feed",
        ),
    ]


def test_category_page_head_uses_the_feed_link_settings(
    default_settings: Settings,
    gen_category_and_html_from_name: Callable,
):
    default_settings["FEED_DOMAIN"] = "https://example.com"
    default_settings["FEED_ATOM"] = "feeds/en.atom.xml"
    default_settings["CATEGORY_FEED_ATOM"] = "feeds/{slug}.atom.xml"
    default_settings["FEED_LINK_TITLES"] = {
        "FEED_ATOM": "Demo — English",
        "CATEGORY_FEED_ATOM": "Demo — English — {name}",
    }
    default_settings["FEED_EXTRA_LINKS"] = (
        ("Demo — All languages", "https://example.com/feeds/all.atom.xml"),
    )

    _, soup = gen_category_and_html_from_name(name="foo", settings=default_settings)

    links = [
        (link["href"], link["title"])
        for link in soup.head.find_all("link", rel="alternate")
    ]
    assert links == [
        ("https://example.com/feeds/en.atom.xml", "Demo — English"),
        ("https://example.com/feeds/all.atom.xml", "Demo — All languages"),
        ("https://example.com/feeds/foo.atom.xml", "Demo — English — foo"),
    ]


@pytest.mark.parametrize("trim", [True, False])
def test_none_settings_are_the_same_as_unset(trim: bool):
    context = {
        "SITENAME": "Site",
        "FEED_DOMAIN": "https://example.com",
        "FEED_ATOM": "feeds/all.atom.xml",
        "CATEGORY_FEED_ATOM": "feeds/{slug}.atom.xml",
        "category": ENTITIES["category"],
    }
    unset = _render(context, trim)

    none = _render(
        {
            **context,
            "FEED_LINK_TITLES": None,
            "FEED_EXTRA_LINKS": None,
            "CATEGORY_TRANSLATIONS": None,
        },
        trim,
    )

    assert none == unset


def test_title_placeholders_other_than_name_are_printed_as_they_are():
    context = {
        "SITENAME": "Site",
        "FEED_DOMAIN": "https://example.com",
        "CATEGORY_FEED_ATOM": "feeds/{slug}.atom.xml",
        "category": SimpleNamespace(name="A&B", slug="a-b"),
        "FEED_LINK_TITLES": {"CATEGORY_FEED_ATOM": "{slug} { {name} {{"},
    }

    (link,) = _links(_render(context))

    assert link[2] == "{slug} { A&B {{"


def test_extra_link_href_is_escaped_and_the_type_is_atom_or_rss():
    context = {
        "SITENAME": "Site",
        "FEED_DOMAIN": "https://example.com",
        "FEED_EXTRA_LINKS": (
            ("Quoted", 'https://example.com/?a=1&b="2"'),
            ("Other", "/x.xml", "xml"),
            ("Upper", "/y.rss", "RSS"),
        ),
    }

    html = _render(context)

    assert 'b="2"' not in html
    assert _links(html) == [
        ("https://example.com/?a=1&b=\"2\"", "application/atom+xml", "Quoted"),
        ("/x.xml", "application/atom+xml", "Other"),
        ("/y.rss", "application/rss+xml", "Upper"),
    ]
