# 작업 로그

위키에 무엇을 언제 했는지 시간순으로 남깁니다. 맨 아래에 추가만 합니다.

## [2026-11-08] setup | 세컨드 브레인 구조
- `blog_src/` → `raw/solar-ess/`로 이동 (drafts/, images/, pptx)
- 나머지 6개 프로젝트의 `raw/<slug>/` 폴더 생성
- `CLAUDE.md` 스키마, `wiki/index.md` 작성

## [2026-11-08] ingest | solar-ess
- 원본: `raw/solar-ess/drafts/00~07`, 부품 조사표
- 생성: [[solar-ess]], [[pv-power-model]], [[peak-sun-hours]], [[ess-battery]], [[sensor-selection]], [[simulation-validation]], [[lessons]]

## [2026-11-08] publish | solar-ess 00~02편
- `docs/blog/posts/solar-ess/` 00~02편 (수동 작성)
- 02편 자리표시 3곳은 "보강 예정"으로 표시 → [[solar-ess]] 미해결 항목

## [2026-11-08] setup | 직접 게시 파이프라인
- `raw/solar-ess/series.toml` + `scripts/build_posts.py` + `Makefile` 도입, CI에서 변환 실행
- 수동 게시본 `docs/blog/posts/solar-ess/` 삭제 → `docs/blog/posts/series/`에서 자동 생성 (URL 동일)
- 02편 부품표: 초안 부품목록을 그대로 접이식 부록으로 붙임
