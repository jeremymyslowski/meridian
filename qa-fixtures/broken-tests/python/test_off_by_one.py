"""Broken test: off-by-one in implementation under test."""

from paginator import paginate


def test_paginate_returns_all_items():
    items = ["a", "b", "c"]
    result = paginate(items, page_size=2)
    # Expect 2 pages: [a,b] and [c]
    assert len(result) == 2
    assert result[-1] == ["c"]