from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pelican.settings import Settings

STYLE_CSS = (
    Path(__file__).parent.parent
    / "src"
    / "pelican"
    / "themes"
    / "attila"
    / "static"
    / "css"
    / "style.css"
)
MAX_WEIGHT = 10


def test_every_weight_the_template_can_emit_has_a_font_size():
    css = STYLE_CSS.read_text()

    missing = [
        weight
        for weight in range(1, MAX_WEIGHT + 1)
        if not re.search(
            rf"\.tag-weight-{weight}\s*\{{[^}}]*font-size:", css
        )
    ]

    # Opacity is defined for 1-10, so a missing font-size means the cloud
    # mixes two scales once TAG_CLOUD_STEPS goes past the refreshed ramp.
    assert not missing, f"tag-weight-N without a font-size: {missing}"


def test_tag_cloud_never_emits_a_weight_class_the_css_does_not_define(
    default_settings: Settings,
    render_direct_template: Callable,
):
    default_settings["TAG_CLOUD_STEPS"] = 40

    soup = render_direct_template("tags", settings=default_settings)

    weights = {
        int(match.group(1))
        for pill in soup.select(".tag-cloud a")
        for cls in pill["class"]
        if (match := re.fullmatch(r"tag-weight-(\d+)", cls))
    }
    assert weights
    assert max(weights) <= MAX_WEIGHT, weights
