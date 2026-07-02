from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader


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
