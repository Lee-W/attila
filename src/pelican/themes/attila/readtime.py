"""Pelican hook that computes a CJK-aware reading time for articles and pages.

The stock word-per-minute estimate breaks on Chinese/Japanese/Korean prose
because those scripts are not space-delimited: an entire article counts as a
handful of "words". This plugin counts CJK characters and non-CJK words as
two separate pools and converts each with its own reading speed.
"""

from __future__ import annotations

import math
import re
from html import unescape

from pelican import signals
from pelican.contents import Article, Page

DEFAULT_CJK_CPM = 300
DEFAULT_WPM = 250

# Letters only: Han ideographs, kana, and Hangul. CJK punctuation and
# fullwidth forms are deliberately excluded from the character count.
_CJK_RE = re.compile(
    "[぀-ヿ"  # Hiragana and Katakana
    "㐀-䶿"  # CJK Unified Ideographs Extension A
    "一-鿿"  # CJK Unified Ideographs
    "가-힣"  # Hangul syllables
    "豈-﫿]"  # CJK Compatibility Ideographs
)
_TAG_RE = re.compile(r"<[^>]+>")
_WORD_RE = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*", re.UNICODE)


def count_text(html: str) -> tuple[int, int]:
    """Return (cjk_characters, non_cjk_words) for a fragment of HTML."""
    text = unescape(_TAG_RE.sub(" ", html))
    cjk_characters = len(_CJK_RE.findall(text))
    words = len(_WORD_RE.findall(_CJK_RE.sub(" ", text)))
    return cjk_characters, words


def _positive_speed(settings, name: str, default: int) -> float:
    """Return a positive finite reading speed from Pelican settings."""
    value = settings.get(name, default)
    try:
        speed = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be a positive number, got {value!r}") from error
    if not math.isfinite(speed) or speed <= 0:
        raise ValueError(f"{name} must be a positive number, got {value!r}")
    return speed


def add_readtime(instance) -> None:
    """Attach ``readtime`` (minutes) and ``readtime_word_count`` to content."""
    if not isinstance(instance, (Article, Page)):
        return
    content = getattr(instance, "_content", None)
    if not content:
        return

    cjk_characters, words = count_text(content)
    if not cjk_characters and not words:
        return

    cpm = _positive_speed(instance.settings, "READTIME_CJK_CPM", DEFAULT_CJK_CPM)
    wpm = _positive_speed(instance.settings, "READTIME_WPM", DEFAULT_WPM)
    instance.readtime = max(1, math.ceil(cjk_characters / cpm + words / wpm))
    instance.readtime_word_count = cjk_characters + words


def register() -> None:
    """Register the per-content hook with Pelican."""
    signals.content_object_init.connect(add_readtime)
