from urllib.parse import urlencode

from playwright.async_api import async_playwright

MUSINSA_RANKING_URL = "https://www.musinsa.com/main/sneaker/ranking"


def build_ranking_url(
    gender: str,
    age_band: str,
    include_soldout: bool = True,
) -> str:
    """요청 조건을 무신사 랭킹 페이지 URL 쿼리로 변환한다."""
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


async def fetch_ranking_html(
    gender: str = "A",
    age_band: str = "AGE_BAND_ALL",
    include_soldout: bool = True,
) -> str:
    """Playwright로 무신사 랭킹 페이지에 접근해 HTML을 가져온다."""
    url = build_ranking_url(
        gender=gender,
        age_band=age_band,
        include_soldout=include_soldout,
    )

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        await page.wait_for_timeout(3_000)
        html = await page.content()

        await browser.close()

    return html
