from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pelican.settings import Settings


def test_plugin_assets_do_not_require_a_literal_plugins_entry(
    default_settings: Settings,
    gen_article_and_html_from_rst: Callable,
):
    # Regression test: with namespace-plugin autodiscovery (PLUGINS unset) or
    # module objects in PLUGINS, "pelican.plugins.osm" never appears as a
    # string, which used to leave the map without its CSS and JS. The markup
    # the plugin emits is the signal that its assets are needed.
    assert not any(
        "osm" in str(plugin) or "heatmap" in str(plugin)
        for plugin in default_settings["PLUGINS"]
    )

    _, soup = gen_article_and_html_from_rst(
        rst_path="content/article_with_plugin_markup.rst",
        settings=default_settings,
    )

    assert soup.select_one('link[href*="leaflet"]') is not None
    assert soup.select_one('script[src*="leaflet"]') is not None
    assert soup.select_one('link[href*="pelican_osm"]') is not None
    assert soup.select_one('script[src*="pelican_osm"]') is not None
    assert soup.select_one('link[href*="pelican_heatmap"]') is not None
    assert soup.select_one('script[src*="pelican_heatmap"]') is not None
