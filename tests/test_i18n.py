from __future__ import annotations

import gettext
import shutil
import subprocess
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

TRANSLATIONS_DIR = (
    Path(__file__).parent.parent
    / "src"
    / "pelican"
    / "themes"
    / "attila"
    / "translations"
)


def test_i18n_macro_passes_interpolation_values_to_newstyle_gettext():
    template_dir = (
        Path(__file__).parent.parent
        / "src"
        / "pelican"
        / "themes"
        / "attila"
        / "templates"
    )
    environment = Environment(
        loader=FileSystemLoader(template_dir),
        extensions=["jinja2.ext.i18n"],
    )
    environment.install_gettext_callables(
        lambda message: message,
        lambda singular, plural, count: singular if count == 1 else plural,
        newstyle=True,
    )
    template = environment.from_string(
        """
        {% import "partials/i18n.html" as i18n with context %}
        {{ i18n.t(
            "Published with %(pelican)s &bull; Theme %(attila)s &bull;",
            pelican="Pelican",
            attila="Attila",
        ) }}
        """
    )

    rendered = template.render(DEFAULT_LANG="en")

    assert "Published with Pelican &bull; Theme Attila &bull;" in rendered


def test_i18n_macro_translates_readtime_messages_to_zh_tw():
    template_dir = (
        Path(__file__).parent.parent
        / "src"
        / "pelican"
        / "themes"
        / "attila"
        / "templates"
    )
    environment = Environment(loader=FileSystemLoader(template_dir))
    template = environment.from_string(
        """
        {% import "partials/i18n.html" as i18n with context %}
        {{ i18n.t("%(count)s min read", count=5) }} / {{ i18n.t("%(count)s words", count="2,300") }}
        """
    )

    rendered = template.render(page_lang="zh-tw", DEFAULT_LANG="en")

    assert "閱讀時間約 5 分鐘 / 共 2,300 字" in rendered


def _load_catalog(mo_path):
    with mo_path.open("rb") as handle:
        # gettext parses the catalog into this attribute and exposes no
        # public accessor for it.
        return gettext.GNUTranslations(handle)._catalog


def test_every_compiled_catalog_keeps_its_po_source():
    orphans = [
        mo_path.parts[-3]
        for mo_path in sorted(TRANSLATIONS_DIR.glob("*/LC_MESSAGES/messages.mo"))
        if not mo_path.with_suffix(".po").exists()
    ]

    assert not orphans, f"messages.mo without a messages.po source: {orphans}"


@pytest.mark.skipif(
    shutil.which("msgfmt") is None, reason="msgfmt (gettext) is not installed"
)
@pytest.mark.parametrize(
    "po_path",
    sorted(TRANSLATIONS_DIR.glob("*/LC_MESSAGES/messages.po")),
    ids=lambda po_path: po_path.parts[-3],
)
def test_compiled_catalog_matches_its_po_source(po_path, tmp_path):
    compiled = tmp_path / "messages.mo"
    subprocess.run(["msgfmt", str(po_path), "-o", str(compiled)], check=True)

    assert _load_catalog(po_path.with_suffix(".mo")) == _load_catalog(compiled), (
        f"{po_path.parts[-3]}: messages.mo is out of sync with messages.po, "
        "run `uv run poe build-i18n`"
    )
