from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup


def test_pelican_cli_builds_theme_without_fixture_translation_setup(tmp_path: Path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pelican",
            "content",
            "-s",
            "default_conf.py",
            "-t",
            "../src/pelican/themes/attila",
            "-o",
            str(tmp_path),
        ],
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / "index.html").is_file()

    for html_path in tmp_path.rglob("*.html"):
        soup = BeautifulSoup(html_path.read_text(), "html.parser")
        assert len(soup.find_all("html")) == 1, html_path
        assert len(soup.find_all("head")) == 1, html_path
        assert len(soup.find_all("body")) == 1, html_path
        ids = [element["id"] for element in soup.select("[id]")]
        assert len(ids) == len(set(ids)), f"duplicate id in {html_path}"
        assert not soup.select('img[src=""]'), html_path
