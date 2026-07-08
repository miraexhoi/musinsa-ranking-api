from bs4 import BeautifulSoup

from app.schemas import RankingItem


def parse_ranking_items(html: str) -> list[RankingItem]:
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")

    items: list[RankingItem] = []
    seen_product_urls = set()

    for link in links:
        href = link.get("href")
        name = link.get_text(" ", strip=True)

        if not href:
            continue

        if "/products/" not in href:
            continue

        if not name:
            continue

        if href in seen_product_urls:
            continue

        seen_product_urls.add(href)

        items.append(
            RankingItem(
                rank=len(items) + 1,
                name=name,
                product_url=href,
            )
        )

    return items


if __name__ == "__main__":
    with open("ranking.html", "r", encoding="utf-8") as file:
        html = file.read()

    items = parse_ranking_items(html)

    print("item count:", len(items))

    for item in items[:20]:
        print(item.model_dump())