from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable

import pytest
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from pelican.settings import Settings

SITEURL = "https://example.com"


@pytest.fixture
def built_output(default_settings: Settings, gen_index_and_html: Callable) -> Path:
    """Build the whole fixture site and return the output directory."""
    default_settings["SITEURL"] = SITEURL
    gen_index_and_html(settings=default_settings)
    return Path("output")


def _canonical(output: Path, relative_path: str) -> str:
    soup = BeautifulSoup((output / relative_path).read_text(), "html.parser")
    links = soup.select('link[rel="canonical"]')
    assert len(links) == 1, relative_path
    return links[0]["href"]


class TestPeriodArchiveCanonical:
    def test_month_archive_points_at_its_zero_padded_url(self, built_output: Path):
        # MONTH_ARCHIVE_SAVE_AS is {date:%Y}/{date:%m}/index.html, so the page
        # lives at /2020/01/ and not at the unpadded, slash-less /2020/1.
        assert _canonical(built_output, "2020/01/index.html") == f"{SITEURL}/2020/01/"

    def test_year_archive_points_at_its_own_url(self, built_output: Path):
        assert _canonical(built_output, "2020/index.html") == f"{SITEURL}/2020/"


class TestPaginatedCanonical:
    def test_first_page_keeps_the_listing_url(self, built_output: Path):
        assert _canonical(built_output, "index.html") == f"{SITEURL}/"
        assert (
            _canonical(built_output, "category/foo/index.html")
            == f"{SITEURL}/category/foo"
        )

    def test_later_index_pages_point_at_themselves(self, built_output: Path):
        assert _canonical(built_output, "page/2/index.html") == f"{SITEURL}/page/2/"

    def test_later_category_pages_point_at_themselves(self, built_output: Path):
        assert (
            _canonical(built_output, "category/foo/page/2/index.html")
            == f"{SITEURL}/category/foo/page/2/"
        )
