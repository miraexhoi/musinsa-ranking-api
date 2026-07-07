# Musinsa Ranking API

무신사 스니커 랭킹 페이지에서 상품 랭킹 데이터를 가져와 API로 반환하는 학습용 FastAPI 프로젝트입니다.

## Why

- Python, FastAPI, Playwright, BeautifulSoup4, Pydantic을 한 프로젝트 안에서 연결하는 흐름을 익히기 위해 필요합니다.
- 무신사 랭킹 페이지는 브라우저에서 동적으로 렌더링될 수 있으므로, 단순 HTTP 요청이 아니라 Playwright 기반 접근을 연습하기 좋습니다.
- 크롤링 결과를 그대로 출력하지 않고 Pydantic schema로 응답 형태를 정의하면, 실무 API처럼 예측 가능한 데이터를 반환할 수 있습니다.
- uv로 의존성을 관리하고 GitHub에 단계별 커밋을 남기면서, 실제 업무 방식에 가까운 개발 흐름을 연습합니다.

## What

- uv 기반의 독립 Python 프로젝트를 구성합니다.
- FastAPI 앱을 만들고 `/rankings` API 엔드포인트를 구현합니다.
- Query Param으로 성별, 연령대, 품절 포함 여부를 전달받습니다.
- Playwright로 무신사 스니커 랭킹 페이지에 접근해 렌더링된 HTML을 가져옵니다.
- BeautifulSoup4로 HTML에서 상품 랭킹 데이터를 파싱합니다.
- Pydantic schema로 API 응답 형태를 정의합니다.
- uvicorn으로 로컬 서버를 실행하고, Swagger UI와 curl로 테스트합니다.

## How

작업은 아래 체크리스트를 기준으로 작게 나눠 진행합니다.

- [x] Step 1. 새 프로젝트 생성 및 uv 초기화
- [x] Step 2. FastAPI, Uvicorn, Playwright, BeautifulSoup4 의존성 설치
- [x] Step 3. FastAPI 기본 앱 생성
- [ ] Step 4. `/rankings` 엔드포인트 뼈대 생성
- [ ] Step 5. Pydantic 응답 schema 정의
- [ ] Step 6. Playwright로 무신사 페이지 HTML 가져오기
- [ ] Step 7. Query Param을 무신사 URL 조건에 반영
- [ ] Step 8. BeautifulSoup4로 상품 데이터 파싱
- [ ] Step 9. 크롤러, 파서, API 연결
- [ ] Step 10. 로컬 실행 및 API 테스트
- [ ] Step 11. README 실행 방법 정리
