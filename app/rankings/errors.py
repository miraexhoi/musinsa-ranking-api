from dataclasses import dataclass


RANKING_FETCH_ERROR_MESSAGE = "Failed to fetch Musinsa ranking page"
RANKING_PARSE_ERROR_MESSAGE = "Failed to parse Musinsa ranking page"


@dataclass
class RankingError(Exception):
    """랭킹 도메인 처리 중 발생한 예외를 표현한다."""

    code: str
    message: str
    status_code: int
    debug_detail: str


class RankingFetchError(RankingError):
    """무신사 랭킹 페이지 수집 실패를 표현한다."""


class RankingParseError(RankingError):
    """무신사 랭킹 HTML 파싱 실패를 표현한다."""
