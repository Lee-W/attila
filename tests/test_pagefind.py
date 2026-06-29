from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from pelican.themes.attila.pagefind import build_index


def test_pagefind_hook_is_disabled_by_default(tmp_path: Path):
    pelican = SimpleNamespace(settings={}, output_path=str(tmp_path))
    with patch("pelican.themes.attila.pagefind._build_index", new=AsyncMock()) as build:
        build_index(pelican)
    build.assert_not_awaited()


def test_pagefind_hook_indexes_pelican_output(tmp_path: Path):
    pelican = SimpleNamespace(
        settings={"PAGEFIND_ENABLED": True, "PAGEFIND_VERBOSE": True},
        output_path=str(tmp_path),
    )
    with patch(
        "pelican.themes.attila.pagefind._build_index",
        new=AsyncMock(return_value=3),
    ) as build:
        build_index(pelican)
    build.assert_awaited_once_with(tmp_path.resolve(), True)
