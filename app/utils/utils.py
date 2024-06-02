from fastapi import Request


def next_page_url(page: int, page_size: int, total: int, request: Request) -> str:
    page_count = total // page_size
    if total % page_size != 0:
        page_count += 1

    next_page_number = page + 1

    if next_page_number > page_count:
        return ""

    next_url = request.url.include_query_params(
        page=str(page + 1),
        page_size=str(page_size),
    )

    return str(next_url)


def previous_page_url(page: int, page_size: int, total: int, request: Request) -> str:
    if page == 1:
        return ""

    page_count = total // page_size
    if total % page_size != 0:
        page_count += 1

    if page > page_count:
        return str(
            request.url.include_query_params(
                page=str(page_count),
                page_size=str(page_size),
            )
        )

    previous_url = request.url.include_query_params(
        page=str(page - 1),
        page_size=str(page_size),
    )

    return str(previous_url)
