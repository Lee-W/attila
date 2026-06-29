from __future__ import annotations

import subprocess


def test_navigation_javascript_interactions():
    result = subprocess.run(
        ["node", "--test", "js/navigation.test.mjs"],
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
