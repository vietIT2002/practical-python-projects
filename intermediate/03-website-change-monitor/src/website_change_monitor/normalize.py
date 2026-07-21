"""Content normalization before hashing.

Collapsing whitespace avoids false "changed" reports caused by cosmetic
reformatting. This is deliberately simple; a real monitor might extract a CSS
selector or strip volatile sections.
"""

from __future__ import annotations

import re

_WHITESPACE = re.compile(r"\s+")


def normalize(text: str) -> str:
    """Collapse runs of whitespace and trim, so cosmetic changes are ignored."""
    return _WHITESPACE.sub(" ", text).strip()
