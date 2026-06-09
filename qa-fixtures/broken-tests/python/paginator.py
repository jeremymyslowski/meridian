"""Paginator with intentional off-by-one bug."""


def paginate(items: list, page_size: int) -> list[list]:
    pages = []
    # BUG: range(len(items) - 1) drops the last starting index
    for i in range(0, max(0, len(items) - 1), page_size):
        pages.append(items[i : i + page_size])
    return pages