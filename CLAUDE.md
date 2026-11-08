# CLAUDE.md — 세컨드 브레인 운영 규칙 (스키마)

이 저장소는 Andrej Karpathy의 **LLM Wiki** 방식으로 운영하는 개인 지식 베이스이자 블로그입니다.
사람은 원본을 모으고 질문을 던지며, LLM은 위키를 정리·유지하고 블로그 원고를 다듬습니다.

## 3개 층

| 층 | 경로 | 주인 | 규칙 |
|---|---|---|---|
| 1. 원본 | `raw/<project>/` | 사람 | **불변.** LLM은 읽기만 한다. 수정·삭제·이름 변경 금지 |
| 2. 위키 | `wiki/` | LLM | 원본을 읽고 요약·개념·교훈으로 컴파일. 사람은 읽고 검토 |
| 3. 출판 | `docs/` | LLM 초안 → 사람 승인 | 위키와 원본에서 다듬은 글만 GitHub Pages로 공개 |

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

새 프로젝트는 이 표, `wiki/index.md`, `mkdocs.yml`의 `categories_allowed`, `docs/projects/index.md`에 함께 추가한다.

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

### 4. Publish — 블로그 게시
"N편까지 게시해줘"라고 하면:
1. 원본 초안(`raw/<project>/drafts/`)을 `docs/blog/posts/<project>/<NN>-<slug>/index.md`로 옮긴다.
2. front matter: `date`(게시일), `slug`(`<project>-<NN>-<영문>`), `categories`(위 표의 카테고리).
3. 첫 문단 뒤에 `<!-- more -->`를 넣는다.
4. 아직 공개 안 된 편으로 가는 링크는 "공개 예정" 텍스트로 바꾼다.
5. 원고의 `[ ... ]` 자리표시는 **지어내지 않는다.** `<span class="todo">보강 예정: ...</span>`으로 바꾸고 위키 미해결 항목에 적는다.
6. 이미지는 쓰이는 것만 글 폴더의 `images/`로 복사한다.
7. `zensical build --clean`이 "No issues found"인지 확인한다.
8. 위키 프로젝트 문서의 출판 현황과 `wiki/log.md`를 갱신한다.

### 5. Update — 수정된 초안 반영
사람이 `raw/<project>/drafts/`의 초안을 고치고 "N편 초안 수정했어, 반영해줘"라고 하면:
1. 해당 초안과 게시본(`docs/blog/posts/<project>/<NN>-*/index.md`)을 비교해 바뀐 부분을 찾는다. 바뀐 내용을 사람에게 요약해 보여준다.
2. Publish 규칙(링크 변환, 자리표시 처리, 이미지 복사)을 그대로 적용해 게시본을 갱신한다. `slug`는 바꾸지 않는다(URL 유지).
3. front matter의 `date`를 아래처럼 바꿔 수정일을 기록한다. 이미 `created`가 있으면 `updated`만 고친다.
   ```yaml
   date:
     created: <최초 게시일시 그대로>
     updated: <오늘 YYYY-MM-DD>
   ```
4. 채워진 자리표시는 위키 미해결 항목에서 체크하고, 바뀐 사실은 위키 프로젝트·개념·교훈 문서에 반영한다.
5. `zensical build --clean` 확인 → `wiki/log.md`에 `## [YYYY-MM-DD] update | <project> N편` 추가.
6. 커밋·push는 사람에게 확인받은 뒤 한다.

`raw/`는 LLM이 수정하지 않는다는 규칙은 그대로다. 초안 수정은 사람만 한다. 사람이 `docs/`의 게시본을 직접 고친 경우에는 덮어쓰기 전에 그 차이를 알리고 초안에 옮길지 묻는다.

## 위키 작성 규칙
- 한국어로 쓴다. 파일명은 영문 kebab-case.
- 문서 맨 위 front matter에 `sources:`(근거 원본 경로)와 `updated:`(YYYY-MM-DD)를 둔다.
- 문서 사이 연결은 Obsidian 호환 `[[파일명]]` 위키링크로 한다.
- 원본에 없는 숫자·사실을 만들지 않는다. 추론은 "추론:"으로 표시한다.
- `wiki/log.md`는 맨 아래에 추가만 한다: `## [YYYY-MM-DD] <작업> | <대상>`.
