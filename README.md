# Unity-lin.github.io — 세컨드 브레인 + 블로그

환경 데이터 프로젝트를 기록하는 개인 지식 베이스이자 블로그입니다.
Andrej Karpathy의 **LLM Wiki**(세컨드 브레인) 방식으로 운영하고, 정리된 내용을 순차적으로 블로그에 게시합니다.

👉 블로그: https://unity-lin.github.io/

## 구조

```
.
├── raw/                    # ① 원본 — 내가 쓰고 고치는 곳 (블로그 글의 진짜 원본)
│   ├── solar-ess/
│   │   ├── series.toml     #    어떤 편을 언제 공개할지 정하는 설정
│   │   ├── drafts/         #    초안 00~07.md
│   │   ├── images/         #    글에 쓰는 그림
│   │   └── *.pptx          #    발표자료 등 참고 원본
│   ├── fine-dust/ urban-heat-island/ rainwater-harvesting/
│   └── river-water-quality/ building-carbon/ food-waste/
├── wiki/                   # ② 위키 — 원본을 정리·연결한 지식 베이스 (Obsidian으로 열 수 있음)
│   ├── index.md            #    전체 목차
│   ├── log.md              #    작업 로그
│   ├── lessons.md          #    프로젝트를 가로지르는 교훈
│   ├── projects/           #    프로젝트별 요약·타임라인·미해결 항목
│   └── concepts/           #    재사용할 개념
├── docs/                   # ③ 사이트 — GitHub Pages로 공개되는 유일한 층
│   ├── index.md, projects/index.md
│   └── blog/posts/
│       ├── series/         #    ⚙️ raw/ 초안에서 자동 생성 (직접 고치지 말 것, git에 안 올라감)
│       └── 2026-11-01-blog-start/   # 시리즈가 아닌 단독 글은 직접 작성
├── scripts/build_posts.py  # raw/ 초안 → docs/blog/posts/series/ 변환기
├── Makefile                # make preview / make publish
├── CLAUDE.md               # Claude가 위키를 관리할 때 지키는 규칙
└── .github/workflows/docs.yml   # push → 변환 → 빌드 → 배포
```

> 저장소가 **공개**이므로 `raw/`, `wiki/`도 GitHub에서 보입니다. 비공개 자료는 넣지 마세요.

## 직접 수정하고 게시하기 (Claude 없이)

### 처음 한 번만

```bash
brew install uv                      # 없다면
uv tool install zensical==0.0.72
```

### 이미 게시된 글 고치기

```bash
# 1. 초안 수정
open raw/solar-ess/drafts/02-하드웨어-도전과-포기.md

# 2. 미리보기 (http://localhost:8000, Ctrl+C로 종료)
make preview

# 3. 게시 (변환 → 오류 검사 → 커밋 → push → 1~2분 뒤 자동 배포)
make publish m="solar-ess 2편 수정"
```

수정일은 자동으로 붙습니다. 초안을 커밋한 날짜가 게시일보다 늦으면 글 상단에 수정일이 표시됩니다.

### 새 편 공개하기

`raw/solar-ess/series.toml`에서 해당 편의 `publish`를 `true`로 바꾸고 `date`를 적습니다.

```toml
[[posts]]
file = "03-시뮬레이터로-방향을-틀다.md"
slug = "solar-ess-03-simulator"     # 주소: /blog/solar-ess-03-simulator/
date = "2026-11-15T09:00:00"        # ← 게시일 입력
publish = true                      # ← false → true
```

```bash
make preview                          # 확인
make publish m="solar-ess 3편 게시"
```

이전 편에 있던 "다음: 3편 *(공개 예정)*" 표시는 자동으로 3편 링크로 바뀝니다.

### 새 프로젝트 시작하기

```bash
mkdir -p raw/fine-dust/drafts raw/fine-dust/images
cp raw/solar-ess/series.toml raw/fine-dust/series.toml   # 복사 후 category와 [[posts]]를 고침
```

`category`는 `mkdocs.yml`의 `categories_allowed`에 있는 이름을 그대로 씁니다(7개 프로젝트는 이미 등록돼 있음).
프로젝트 목록 페이지 `docs/projects/index.md`의 상태 칸도 함께 고쳐 주세요.

### 명령어 요약

| 명령 | 하는 일 |
|---|---|
| `make preview` | 초안 → 블로그 글 변환 후 로컬 미리보기 |
| `make build` | 변환 + 빌드 오류 검사만 (커밋 안 함) |
| `make publish m="메시지"` | 변환 + 검사 + `git add/commit/push` → 자동 배포 |
| `gh run watch` | 배포 진행 상황 보기 (선택) |

`make` 없이 `git push`만 해도 GitHub Actions가 같은 변환을 실행하므로 블로그에 반영됩니다. `make publish`는 push 전에 오류를 미리 잡아 줍니다.
반영이 안 보이면 브라우저에서 `⌘ + Shift + R`(강력 새로고침)을 누르세요.

## 초안 작성 규칙

변환기(`scripts/build_posts.py`)가 아래 문법을 블로그 형식으로 바꿉니다.

| 초안에 쓰는 것 | 블로그에서 |
|---|---|
| `# 2편. 제목` | 글 제목 |
| 제목 다음 첫 문단 | 목록 페이지에 보이는 요약 |
| `[다음 편](03-시뮬레이터로-방향을-틀다.md)` | 공개된 편이면 링크, 아니면 "다음 편 *(공개 예정)*" |
| `` `[ 조립 사진 ]` `` (백틱 + 대괄호 + 공백) | 점선 상자 "보강 예정: 조립 사진" |
| `![설명](images/chart.svg)` | 그림 (`raw/<project>/images/`에서 자동 복사) |
| `<!-- 메모 -->` | 숨김 (블로그에 안 보임) |
| `!!! tip "제목"` + 4칸 들여쓴 본문 | 강조 상자 ([문법](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)) |

## Claude와 함께 쓸 때 (선택)

직접 게시와 별개로, 위키 정리는 Claude에게 맡길 수 있습니다. 규칙은 [CLAUDE.md](CLAUDE.md)에 있습니다.

| 입력 | 결과 |
|---|---|
| `solar-ess ingest 해줘` | 새 원본을 읽고 위키(프로젝트·개념·교훈·로그) 갱신 |
| `위키 점검해줘` | 모순, 끊긴 링크, 오래된 내용 확인 |
| `<질문>` | 위키를 근거로 답하고, 좋은 답은 위키에 저장 |

## 진행 현황

| 프로젝트 | 원본 | 위키 | 블로그 |
|---|---|---|---|
| 태양광 ESS 시뮬레이터 | ✅ 8편 원고 | ✅ | 0~2편 공개 / 3~7편 대기 |
| 미세먼지 추적 | — | — | — |
| 도시 열섬 지도 | — | — | — |
| 빗물저장 시뮬레이터 | — | — | — |
| 하천 수질 모니터링 | — | — | — |
| 건물 탄소 발자국 | — | — | — |
| 음식물쓰레기 감량효과 | — | — | — |
