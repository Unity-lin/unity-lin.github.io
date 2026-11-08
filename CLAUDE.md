# CLAUDE.md — 세컨드 브레인 운영 규칙 (스키마)

이 저장소는 Andrej Karpathy의 **LLM Wiki** 방식으로 운영하는 개인 지식 베이스이자 블로그입니다.
사람은 원본을 모으고 질문을 던지며, LLM은 위키를 정리·유지하고 블로그 원고를 다듬습니다.

## 3개 층

| 층 | 경로 | 주인 | 규칙 |
|---|---|---|---|
| 1. 원본 | `raw/<project>/` | 사람 | 사람이 직접 쓰고 고친다. LLM은 읽기만 한다(예외: 부탁받았을 때 `series.toml`의 publish/date) |
| 2. 위키 | `wiki/` | LLM | 원본을 읽고 요약·개념·교훈으로 컴파일. 사람은 읽고 검토 |
| 3. 출판 | `docs/` | 자동 생성 + 사람 | 시리즈 글은 `raw/`에서 자동 생성, 홈·프로젝트 페이지·단독 글은 직접 작성 |

`raw/`와 `wiki/`는 MkDocs 빌드 대상이 아니다(`docs/`만 사이트가 된다). 단, 저장소는 공개이므로 `raw/`에 비공개 자료를 넣지 않는다.

## 프로젝트 슬러그

| 슬러그 | 프로젝트 | 블로그 카테고리 |
|---|---|---|
| `solar-ess` | 태양광 ESS 시뮬레이터 | 태양광 ESS 시뮬레이터 |
| `fine-dust` | 미세먼지 추적 | 미세먼지 추적 |
| `urban-heat-island` | 도시 열섬 지도 | 도시 열섬 지도 |
| `rainwater-harvesting` | 빗물저장 시뮬레이터 | 빗물저장 시뮬레이터 |
| `river-water-quality` | 하천 수질 모니터링 | 하천 수질 모니터링 |
| `building-carbon` | 건물 탄소 발자국 | 건물 탄소 발자국 |
| `food-waste` | 음식물쓰레기 감량효과 | 음식물쓰레기 감량효과 |

새 프로젝트는 이 표, `raw/<slug>/series.toml`, `wiki/index.md`, `mkdocs.yml`의 `categories_allowed`, `docs/projects/index.md`에 함께 추가한다.

## 작업 (Operations)

### 1. Ingest — 원본 흡수
사람이 `raw/<project>/`에 자료를 넣고 "ingest 해줘"라고 하면:
1. 새 원본을 끝까지 읽는다.
2. `wiki/projects/<project>.md`를 만들거나 갱신한다(개요, 타임라인, 구조, 미해결 항목, 출판 현황).
3. 여러 프로젝트에 쓰일 지식은 `wiki/concepts/`에 개념 문서로 뽑고, 기존 문서가 있으면 고친다.
4. 배운 점은 `wiki/lessons.md`에 출처와 함께 추가한다.
5. `wiki/index.md` 목록과 `wiki/log.md`를 갱신한다.

### 2. Query — 질문
질문에는 `wiki/index.md`부터 읽고 위키를 근거로 답한다. 답이 재사용할 만하면 위키 문서로 남긴다.

### 3. Lint — 점검
요청 시 위키를 점검한다: 원본과 어긋난 내용, 끊긴 `[[링크]]`, 고아 문서, 오래된 상태값, 문서 사이 모순.

### 4. Publish / Update — 블로그 게시 (사람이 직접 함)
게시는 자동 파이프라인으로 한다. **`docs/blog/posts/series/`는 생성물이므로 직접 고치지 않는다.**
- 원본: `raw/<project>/drafts/*.md` + `raw/<project>/series.toml`(공개 여부·slug·게시일)
- 변환: `scripts/build_posts.py` — 링크 변환, `` `[ … ]` `` → "보강 예정", `<!-- more -->`, 이미지 복사, appendix, git 기록 기반 수정일
- 명령: `make preview` / `make build` / `make publish m="..."`. CI(`.github/workflows/docs.yml`)도 같은 변환을 실행한다.

사람이 게시를 부탁하면 Claude는 `series.toml`의 `publish`/`date`만 바꾸고 `make build`로 확인한다. 초안 본문은 고치지 않는다. 게시 후 위키 프로젝트 문서의 출판 현황과 `wiki/log.md`를 갱신한다.
변환 규칙을 바꿀 때는 `scripts/build_posts.py`와 README의 "초안 작성 규칙" 표를 함께 고친다.

## 위키 작성 규칙
- 한국어로 쓴다. 파일명은 영문 kebab-case.
- 문서 맨 위 front matter에 `sources:`(근거 원본 경로)와 `updated:`(YYYY-MM-DD)를 둔다.
- 문서 사이 연결은 Obsidian 호환 `[[파일명]]` 위키링크로 한다.
- 원본에 없는 숫자·사실을 만들지 않는다. 추론은 "추론:"으로 표시한다.
- `wiki/log.md`는 맨 아래에 추가만 한다: `## [YYYY-MM-DD] <작업> | <대상>`.
