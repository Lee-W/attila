"""The no-gettext branches of partials/i18n.html.

The default JINJA_ENVIRONMENT does not load jinja2.ext.i18n, so a normal
build renders every string through these hand-written branches.
"""

from __future__ import annotations

import gettext
import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

THEME_DIR = Path(__file__).parent.parent / "src" / "pelican" / "themes" / "attila"
TEMPLATE_DIR = THEME_DIR / "templates"

_ENVIRONMENT = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def _translate(message: str, lang: str, **kwargs: object) -> str:
    template = _ENVIRONMENT.from_string(
        '{% import "partials/i18n.html" as i18n with context %}'
        "{{ i18n.t(message, **kwargs) }}"
    )
    return template.render(
        message=message, kwargs=kwargs, page_lang=lang, DEFAULT_LANG="en"
    ).strip()


@pytest.mark.parametrize("lang", ["en", "ja"])
def test_post_count_is_interpolated_outside_zh(lang: str):
    assert _translate("%(count)s Posts", lang, count=7) == "7 Posts"


@pytest.mark.parametrize("lang", ["zh-tw", "zh-TW", "zh_tw", "zh", "zh-hant"])
def test_post_count_is_translated_for_every_zh_variant(lang: str):
    assert _translate("%(count)s Posts", lang, count=7) == "7 篇文章"


@pytest.mark.parametrize(
    ("message", "expected"), [("Newer", "較新"), ("Older", "較舊")]
)
def test_post_navigation_labels_are_translated_in_zh(message: str, expected: str):
    assert _translate(message, "zh-tw") == expected


def _template_message_ids() -> set[str]:
    pattern = re.compile(r"""i18n\.t\(\s*(?:"((?:[^"\\]|\\.)*)"|'([^']*)')""")
    found: set[str] = set()
    for path in TEMPLATE_DIR.rglob("*.html"):
        for double, single in pattern.findall(path.read_text()):
            found.add((double or single).replace('\\"', '"'))
    return found


def _po_message_ids(lang: str) -> set[str]:
    mo_path = THEME_DIR / "translations" / lang / "LC_MESSAGES" / "messages.mo"
    with mo_path.open("rb") as handle:
        catalog = gettext.GNUTranslations(handle)._catalog
    return {key for key in catalog if isinstance(key, str) and key}


@pytest.mark.parametrize("message", sorted(_template_message_ids()))
def test_every_template_message_translated_by_the_catalog_is_translated_by_the_zh_fallback(
    message: str,
):
    if message not in _po_message_ids("zh-tw"):
        pytest.skip("not translated in the zh-tw catalog either")

    rendered = _translate(
        message,
        "zh-tw",
        current=1,
        total=2,
        count=3,
        index=1,
        name="Series",
        pelican="Pelican",
        attila="Attila",
    )
    assert rendered != message, f"zh fallback renders {message!r} untranslated"
