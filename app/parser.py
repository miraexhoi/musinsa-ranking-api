from bs4 import BeautifulSoup


def parse_ranking_items(html: str) -> list[dict[str, int | str]]:
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")

    items = []
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
            {
                "rank": len(items) + 1,
                "name": name,
                "product_url": href,
            }
        )

    return items


if __name__ == "__main__":
    with open("ranking.html", "r", encoding="utf-8") as file:
        html = file.read()

    items = parse_ranking_items(html)

    print("item count:", len(items))

    for item in items[:20]:
        print(item)