"""Pelican hook that builds the Pagefind search bundle after site generation."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from pelican import signals

logger = logging.getLogger("attila.pagefind")


async def _build_index(output_path: Path, verbose: bool) -> int:
    try:
        from pagefind.index import IndexConfig, PagefindIndex
    except ImportError as error:
        raise RuntimeError(
            "PAGEFIND_ENABLED requires the extended Pagefind package: "
            "pip install 'pagefind[extended]>=1.5.2'"
        ) from error

    config = IndexConfig(
        output_path=str(output_path / "pagefind"),
        verbose=verbose,
    )
    async with PagefindIndex(config=config) as index:
        result = await index.add_directory(str(output_path))
        return int(result.get("page_count", 0))


def build_index(pelican) -> None:
    """Build the static search index when PAGEFIND_ENABLED is true."""
    if not pelican.settings.get("PAGEFIND_ENABLED", False):
        return

    output_path = Path(pelican.output_path).resolve()
    page_count = asyncio.run(
        _build_index(output_path, bool(pelican.settings.get("PAGEFIND_VERBOSE", False)))
    )
    logger.info("Pagefind indexed %d page(s) in %s", page_count, output_path)


def register() -> None:
    """Register the post-build indexing hook with Pelican."""
    signals.finalized.connect(build_index)
