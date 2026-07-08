from app.rankings.parser import parse_ranking_items


def test_parse_ranking_items_extracts_product_card():
    html = """
    <div
        data-item-id="4207634"
        data-price="52800"
        data-item-list-index="1"
    >
        <a href="https://www.musinsa.com/products/4207634">
            <img src="https://image.msscdn.net/sample.jpg" />
        </a>
        <a href="https://www.musinsa.com/brand/actplus">
            <p>액트플러스</p>
        </a>
        <a href="https://www.musinsa.com/products/4207634">
            얼라인플러스 하이드로 블립온 트루 블랙
        </a>
    </div>
    """

    items = parse_ranking_items(html)

    assert len(items) == 1

    item = items[0]
    assert item.rank == 1
    assert item.name == "얼라인플러스 하이드로 블립온 트루 블랙"
    assert item.product_url == "https://www.musinsa.com/products/4207634"
    assert item.brand == "액트플러스"
    assert item.price == 52800
    assert item.image_url == "https://image.msscdn.net/sample.jpg"
    assert item.is_soldout is False


def test_parse_ranking_items_marks_soldout_item():
    html = """
    <div
        data-item-id="123"
        data-price="10000"
        data-item-list-index="1"
    >
        <a href="https://www.musinsa.com/brand/test">
            <p>테스트브랜드</p>
        </a>
        <a href="https://www.musinsa.com/products/123">
            테스트 상품
        </a>
        <span>품절</span>
    </div>
    """

    items = parse_ranking_items(html)

    assert len(items) == 1
    assert items[0].is_soldout is True