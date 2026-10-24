from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable

import pytest
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from pelican.settings import Settings
    from pelican.writers import Writer


def _read(output: Path, relative_path: str) -> BeautifulSoup:
    return BeautifulSoup((output / relative_path).read_text(), "html.parser")


@pytest.fixture
def built_output(
    default_settings: Settings, default_writer: Writer, gen_index_and_html: Callable
) -> Path:
    gen_index_and_html(settings=default_settings)
    return Path(default_writer.output_path)


def test_month_banner_uses_the_translated_month_label(built_output: Path):
    soup = _read(built_output, "2020/01/index.html")
    assert soup.select_one(".banner-title").get_text(strip=True) == "January 2020"
    assert "January 2020" in soup.title.get_text()
    # Same wording as the per-month divider inside the listing.
    assert soup.select_one(".post-month-label").get_text(strip=True) == "January 2020"


def test_year_banner_stays_just_the_year(built_output: Path):
    soup = _read(built_output, "2020/index.html")
    assert soup.select_one(".banner-title").get_text(strip=True) == "2020"
