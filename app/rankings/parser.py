from bs4 import BeautifulSoup

from app.rankings.schemas import RankingItem


def parse_price(value: str | None) -> int | None:
    """HTML 속성의 가격 문자열을 정수로 변환한다."""
    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def parse_rank(value: str | None, fallback_rank: int) -> int:
    """HTML 속성의 랭킹 문자열을 정수로 변환한다."""
    if value is None:
        return fallback_rank

    try:
        return int(value)
    except ValueError:
        return fallback_rank


def parse_is_soldout(card) -> bool:
    """상품 카드 텍스트에서 품절 여부를 판단한다."""
    text = card.get_text(" ", strip=True)
    return "품절" in text or "SOLD OUT" in text.upper()


def parse_ranking_items(html: str) -> list[RankingItem]:
    """무신사 랭킹 HTML에서 상품 랭킹 목록을 추출한다."""
    soup = BeautifulSoup(html, "html.parser")

    cards = soup.find_all(
        attrs={
            "data-item-id": True,
            "data-price": True,
            "data-item-list-index": True,
        }
    )

    items: list[RankingItem] = []
    seen_product_urls = set()

    for card in cards:
        item_id = card.get("data-item-id")
        price = parse_price(card.get("data-price"))
        rank = parse_rank(card.get("data-item-list-index"), len(items) + 1)

        if not item_id:
            continue

        product_url = f"https://www.musinsa.com/products/{item_id}"

        if product_url in seen_product_urls:
            continue

        product_links = card.find_all("a", href=product_url)

        if card.name == "a" and card.get("href") == product_url:
            product_links.append(card)

        name = ""

        for product_link in product_links:
            text = product_link.get_text(" ", strip=True)

            if text:
                name = text
                break

        if not name:
            continue

        brand_link = card.find("a", href=lambda href: href and "/brand/" in href)
        brand = brand_link.get_text(" ", strip=True) if brand_link else None

        image = card.find("img")
        image_url = image.get("src") if image else None

        seen_product_urls.add(product_url)

        items.append(
            RankingItem(
                rank=rank,
                brand=brand,
                name=name,
                price=price,
                product_url=product_url,
                image_url=image_url,
                is_soldout=parse_is_soldout(card),
            )
        )

    return items
