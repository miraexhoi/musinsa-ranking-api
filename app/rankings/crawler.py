from urllib.parse import urlencode

from playwright.sync_api import sync_playwright

MUSINSA_RANKING_URL = "https://www.musinsa.com/main/sneaker/ranking"

def build_ranking_url(
    gender: str,
    age_band: str,
    include_soldout: bool = True,
) -> str:
    query_params = {
        "gf": gender,
        "storeCode": "sneaker",
        "sectionId": "256",
        "contentsId": "",
        "categoryCode": "103000",
        "ageBand": age_band,
        "soldOut": str(include_soldout).lower(),
    }

    return f"{MUSINSA_RANKING_URL}?{urlencode(query_params)}"

def fetch_ranking_html(
    gender: str = "A",
    age_band: str = "AGE_BAND_ALL",
    include_soldout: bool = True,
) -> str:
    url = build_ranking_url(
        gender=gender,
        age_band=age_band,
        include_soldout=include_soldout,
    )

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        page.wait_for_timeout(3_000)
        html = page.content()

        browser.close()

    return html
