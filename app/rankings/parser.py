from fastapi import status
from bs4 import BeautifulSoup

from app.rankings.errors import RANKING_PARSE_ERROR_MESSAGE, RankingParseError
from app.rankings.schemas import RankingItem


def parse_price(value: str | None) -> int | None:
    """HTML 속성의 가격 문자열을 정수로 변환한다."""
    if value is None:
        return None

    try:
        return int(value)
    except ValueError as error:
        raise RankingParseError(
            code="RANKING_PRICE_PARSE_FAILED",
            message=RANKING_PARSE_ERROR_MESSAGE,
            status_code=status.HTTP_502_BAD_GATEWAY,
            debug_detail=f"data-price value is not numeric: value={value}",
        ) from error


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


def parse_ranking_item(card, fallback_rank: int) -> RankingItem:
    """상품 카드 하나에서 랭킹 상품 정보를 추출한다."""
    item_id = card.get("data-item-id")

    if not item_id:
        raise RankingParseError(
            code="RANKING_ITEM_ID_NOT_FOUND",
            message=RANKING_PARSE_ERROR_MESSAGE,
            status_code=status.HTTP_502_BAD_GATEWAY,
            debug_detail=f"data-item-id attribute is missing: rank={fallback_rank}",
        )

    product_url = f"https://www.musinsa.com/products/{item_id}"
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
        raise RankingParseError(
            code="RANKING_ITEM_NAME_NOT_FOUND",
            message=RANKING_PARSE_ERROR_MESSAGE,
            status_code=status.HTTP_502_BAD_GATEWAY,
            debug_detail=(
                "Product name link text is missing: "
                f"rank={fallback_rank}, product_url={product_url}"
            ),
        )

    brand_link = card.find("a", href=lambda href: href and "/brand/" in href)
    brand = brand_link.get_text(" ", strip=True) if brand_link else None

    image = card.find("img")
    image_url = image.get("src") if image else None

    return RankingItem(
        rank=parse_rank(card.get("data-item-list-index"), fallback_rank),
        brand=brand,
        name=name,
        price=parse_price(card.get("data-price")),
        product_url=product_url,
        image_url=image_url,
        is_soldout=parse_is_soldout(card),
    )


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

    if not cards:
        raise RankingParseError(
            code="RANKING_CARD_NOT_FOUND",
            message=RANKING_PARSE_ERROR_MESSAGE,
            status_code=status.HTTP_502_BAD_GATEWAY,
            debug_detail=(
                "No product cards found by attributes: "
                "data-item-id, data-price, data-item-list-index"
            ),
        )

    items: list[RankingItem] = []
    seen_product_urls = set()

    for card in cards:
        try:
            item = parse_ranking_item(card, fallback_rank=len(items) + 1)
        except RankingParseError:
            raise
        except Exception as error:
            raise RankingParseError(
                code="RANKING_CARD_PARSE_FAILED",
                message=RANKING_PARSE_ERROR_MESSAGE,
                status_code=status.HTTP_502_BAD_GATEWAY,
                debug_detail=(
                    "Unexpected error while parsing product card: "
                    f"rank={len(items) + 1}, error={error}"
                ),
            ) from error

        if item.product_url in seen_product_urls:
            continue

        seen_product_urls.add(item.product_url)
        items.append(item)

    if not items:
        raise RankingParseError(
            code="RANKING_ITEM_NOT_FOUND",
            message=RANKING_PARSE_ERROR_MESSAGE,
            status_code=status.HTTP_502_BAD_GATEWAY,
            debug_detail="Product cards were found, but no ranking items were parsed.",
        )

    return items
