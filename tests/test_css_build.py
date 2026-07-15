from __future__ import annotations

import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS_SRC = REPO_ROOT / "css-src"
STYLE_CSS = REPO_ROOT / "src/pelican/themes/attila/static/css/style.css"


def test_style_css_matches_sources():
    """The shipped style.css must equal the concatenation of css-src/*.css.

    Edit the modules in css-src/ and run `uv run poe build-css`; the generated
    style.css is never edited directly. This test guards against drift.
    """
    parts = sorted(CSS_SRC.glob("*.css"))
    assert parts, "no css-src/*.css modules found"
    rebuilt = "".join(part.read_text() for part in parts)
    assert STYLE_CSS.read_text() == rebuilt, (
        "style.css is out of sync with css-src/. Run `uv run poe build-css`."
    )


def test_navigation_uses_a_single_tablet_breakpoint():
    theme = (CSS_SRC / "05-theme.css").read_text()
    refresh = (CSS_SRC / "05a-refresh.css").read_text()

    assert re.search(
        r"@media only screen and \(max-width: 768px\) \{\s*"
        r"\.nav-header \{\s*transform: translate3d\(0, -100%, 0\)",
        theme,
    )
    assert re.search(
        r"@media only screen and \(max-width: 768px\) \{\s*"
        r"\.nav-wrapper-control \{\s*display: block",
        theme,
    )
    assert "@media (min-width: 769px)" in refresh


def test_mobile_post_header_keeps_padding_inside_viewport_width():
    refresh = (CSS_SRC / "05a-refresh.css").read_text()
    assert re.search(
        r"\.post-header,\s*\.post-header\.has-cover \{\s*"
        r"box-sizing: border-box;\s*display: block;",
        refresh,
    )


def test_listing_banner_title_has_multiline_spacing():
    refresh = (CSS_SRC / "05a-refresh.css").read_text()
    assert re.search(
        r"\.site-banner \.banner-title \{\s*"
        r"margin: 0;\s*font-size: 37px;\s*line-height: 1\.2;",
        refresh,
    )


def test_inlined_icon_sprite_matches_the_sprite_file():
    """The templates inline the sprite; the standalone file must not drift from it.

    Both artifacts come from `node scripts/build_icon_sprite.mjs ... OUTPUT PARTIAL`.
    The inlined copy is what pages actually reference: WebKit does not resolve
    <use> across documents, so an external sprite renders blank on iOS.
    """
    theme = REPO_ROOT / "src/pelican/themes/attila"
    sprite = (theme / "static/icons/icons.svg").read_text()
    partial = (theme / "templates/partials/icon-sprite.html").read_text()

    symbols = re.findall(r'<symbol id="([^"]+)"', sprite)
    assert symbols, "no symbols found in icons.svg"
    assert re.findall(r'<symbol id="([^"]+)"', partial) == symbols, (
        "icon-sprite.html is out of sync with icons.svg. Re-run "
        "scripts/build_icon_sprite.mjs to regenerate both."
    )
