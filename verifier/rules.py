def expected(data):
    pages = {page.id: page for page in data.pages}
    rows = []
    for claim in sorted(data.claims, key=lambda item: item.id):
        page = pages.get(claim.page_id)
        if page is None:
            reason = "missing_page"
        elif page.http_status != 200:
            reason = "http_error"
        elif claim.url != page.url:
            reason = "url_mismatch"
        elif not claim.excerpt:
            reason = "empty_excerpt"
        elif claim.excerpt not in page.text:
            reason = "nonverbatim"
        else:
            reason = "verified"
        rows.append({"claim_id": claim.id, "reason": reason})
    return {"rows": rows}
