# Musinsa Ranking API

무신사 스니커즈 랭킹 페이지에서 상품 랭킹 데이터를 가져와 API로 반환하는 FastAPI 프로젝트입니다.

## WHY

- Python, FastAPI, Playwright, BeautifulSoup4, Pydantic을 한 프로젝트 안에서 연결하는 흐름을 익히기 위해 필요합니다.
- 무신사 랭킹 페이지는 브라우저에서 동적으로 렌더링될 수 있으므로, 단순 HTTP 요청이 아니라 Playwright 기반 접근을 연습하기 좋습니다.
- 크롤링 결과를 그대로 출력하지 않고 Pydantic schema로 응답 형태를 정의하면, 실무 API처럼 예측 가능한 데이터를 반환할 수 있습니다.

## WHAT

- uv 기반의 독립 Python 프로젝트를 구성합니다.
- FastAPI 앱을 만들고 `/rankings` API 엔드포인트를 구현합니다.
- Query Param으로 성별, 연령대, 품절 포함 여부를 전달받습니다.
- Playwright로 무신사 스니커 랭킹 페이지에 접근해 렌더링된 HTML을 가져옵니다.
- BeautifulSoup4로 HTML에서 상품 랭킹 데이터를 파싱합니다.
- Pydantic schema로 API 응답 형태를 정의합니다.
- uvicorn으로 로컬 서버를 실행하고, Swagger UI와 curl로 테스트합니다.

## HOW

작업은 아래 체크리스트를 기준으로 작게 나눠 진행합니다.

- [x] Step 1. 새 프로젝트 생성 및 uv 초기화
- [x] Step 2. FastAPI, Uvicorn, Playwright, BeautifulSoup4 의존성 설치
- [x] Step 3. FastAPI 기본 앱 생성
- [x] Step 4. `/rankings` 엔드포인트 뼈대 생성
- [x] Step 5. Pydantic 응답 schema 정의
- [x] Step 6. Playwright로 무신사 페이지 HTML 가져오기
- [x] Step 7. Query Param을 무신사 URL 조건에 반영
- [x] Step 8. BeautifulSoup4로 상품 데이터 파싱
- [x] Step 9. 크롤러, 파서, API 연결
- [x] Step 10. 로컬 실행 및 API 테스트
- [x] Step 11. README 실행 방법 정리

## Feedback Checklist

- [x] 폴더 구조 개선
- [x] 파일 단독 실행용 `__name__` 블록 제거
- [ ] 비동기 적용
- [ ] 테스트 코드 작성
- [ ] 예외 처리 구조 개선
- [ ] 엔드포인트 및 함수 네이밍 컨벤션 정리
- [ ] Documentation 정리

## Project Structure

```text
app/
├── __init__.py
├── crawler.py   # Playwright로 무신사 랭킹 페이지 HTML을 가져옵니다.
├── main.py      # FastAPI 앱과 /rankings 엔드포인트를 정의합니다.
├── parser.py    # BeautifulSoup4로 HTML에서 상품 데이터를 추출합니다.
└── schemas.py   # Pydantic으로 API 응답 형태를 정의합니다.
```

## Setup

의존성 설치:

```bash
uv sync
```

Playwright 브라우저 설치:

```bash
uv run playwright install chromium
```

## Run

서버 실행:

```bash
uv run uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl "http://127.0.0.1:8000/health"
```

## API

### GET `/rankings`

무신사 스니커 랭킹 페이지에 접근해 상품 랭킹 목록을 반환합니다.

Query Params:

| Name | Example | Description |
| --- | --- | --- |
| `gender` | `A`, `M`, `F` | 성별 조건입니다. 무신사 URL의 `gf` 값으로 전달합니다. |
| `age_band` | `AGE_BAND_ALL` | 연령대 조건입니다. 무신사 URL의 `ageBand` 값으로 전달합니다. |
| `include_soldout` | `true`, `false` | 품절 상품 포함 여부입니다. 무신사 URL의 `soldOut` 값으로 전달하고, 응답에서도 한 번 더 필터링합니다. |

요청 예시:

```bash
curl "http://127.0.0.1:8000/rankings?gender=A&age_band=AGE_BAND_ALL&include_soldout=true"
```

보기 좋게 출력:

```bash
curl "http://127.0.0.1:8000/rankings?gender=A&age_band=AGE_BAND_ALL&include_soldout=true" | python -m json.tool
```

응답 예시:

```json
{
  "gender": "A",
  "age_band": "AGE_BAND_ALL",
  "include_soldout": true,
  "count": 24,
  "items": [
    {
      "rank": 1,
      "name": "얼라인플러스 하이드로 블립온 트루 블랙",
      "product_url": "https://www.musinsa.com/products/4207634",
      "brand": "액트플러스",
      "price": 52800,
      "image_url": "https://image.msscdn.net/thumbnails/images/goods_img/20240619/4207634/4207634_17187846410655_500.jpg?w=780",
      "is_soldout": false
    }
  ]
}
```
