from urllib.parse import urlencode

from playwright.sync_api import sync_playwright

MUSINSA_RANKING_URL = "https://www.musinsa.com/main/sneaker/ranking"

def build_ranking_url(gender: str, age_band:str) -> str:
    query_params = {
        "gf": gender,
        "storeCode": "sneaker",
        "sectionId": "256",
        "contentsId": "",
        "categoryCode": "103000",
        "ageBand": age_band,
    }

    return f"{MUSINSA_RANKING_URL}?{urlencode(query_params)}"

def fetch_ranking_html(gender: str = "A", age_band: str = "AGE_BAND_ALL") -> str:
    url = build_ranking_url(gender=gender, age_band=age_band)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        page.wait_for_timeout(3_000)
        html = page.content()

        browser.close()

    return html

if __name__ == "__main__":
    html = fetch_ranking_html()

    with open("ranking.html", "w", encoding="utf-8") as file:
        file.write(html)

    print("Saved ranking.html")
    print(f"HTML length: {len(html)}")
