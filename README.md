# Unity-lin.github.io — 세컨드 브레인 + 블로그

환경 데이터 프로젝트를 기록하는 개인 지식 베이스이자 블로그입니다.
Andrej Karpathy의 **LLM Wiki**(세컨드 브레인) 방식으로 운영하고, 정리된 내용을 순차적으로 블로그에 게시합니다.

👉 블로그: https://unity-lin.github.io/

## 구조

```
.
├── CLAUDE.md          # 스키마: LLM이 위키를 관리하고 글을 게시하는 규칙
├── raw/               # ① 원본 (사람이 넣고, 수정하지 않음)
│   ├── solar-ess/     #    태양광 ESS 시뮬레이터 — drafts/, images/, 발표자료.pptx
│   ├── fine-dust/     #    미세먼지 추적
│   ├── urban-heat-island/
│   ├── rainwater-harvesting/
│   ├── river-water-quality/
│   ├── building-carbon/
│   └── food-waste/
├── wiki/              # ② 위키 (LLM이 원본을 정리·연결. Obsidian으로 열 수 있음)
│   ├── index.md       #    전체 목차 — 질문은 여기서 시작
│   ├── log.md         #    작업 로그 (시간순, 추가만)
│   ├── lessons.md     #    프로젝트를 가로지르는 교훈
│   ├── projects/      #    프로젝트별 요약·타임라인·미해결 항목·출판 현황
│   └── concepts/      #    재사용할 개념 (PV 모델, PSH, ESS, 센서, 검증)
├── docs/              # ③ 출판 (MkDocs → GitHub Pages로 공개되는 유일한 층)
│   ├── index.md
│   ├── projects/index.md
│   └── blog/posts/<project>/<NN>-<slug>/index.md
├── mkdocs.yml
└── .github/workflows/docs.yml   # main push → 자동 배포
```

| 층 | 누가 쓰나 | 공개 |
|---|---|---|
| `raw/` | 나 | 저장소에만 (사이트 X) |
| `wiki/` | LLM이 쓰고 내가 검토 | 저장소에만 (사이트 X) |
| `docs/` | LLM 초안, 내가 승인 | 사이트로 공개 |

> 저장소가 **공개**이므로 `raw/`, `wiki/`도 GitHub에서 보입니다. 비공개 자료는 넣지 마세요.

## 작업 흐름

1. **모으기** — 메모, 원고, 그림, 발표자료를 `raw/<project>/`에 넣는다.
2. **Ingest** — Claude에게 "`<project>` ingest 해줘" → 위키 프로젝트 문서·개념·교훈·로그 갱신
3. **Query** — 위키를 근거로 질문하고, 좋은 답은 위키 문서로 남긴다.
4. **Lint** — "위키 점검해줘" → 모순, 끊긴 링크, 오래된 내용 확인
5. **Publish** — "`<project>` N편까지 게시해줘" → `docs/blog/posts/`에 글 생성 → 빌드 확인 → push
6. **Update** — 초안을 고친 뒤 "`<project>` N편 초안 수정했어, 반영해줘" → 게시본·위키 갱신 (아래 참고)

자세한 규칙은 [CLAUDE.md](CLAUDE.md)에 있습니다.

## 초안을 고친 뒤 블로그에 반영하기

원고의 원본은 `raw/<project>/drafts/`의 초안입니다. **초안을 먼저 고치고**, 게시된 글은 초안에서 다시 만듭니다. (`docs/`의 글을 직접 고치면 다음 게시 때 초안 내용으로 덮어써질 수 있습니다.)

### 1) 초안 수정

```bash
open raw/solar-ess/drafts/02-하드웨어-도전과-포기.md   # 원하는 편집기로 수정
```

### 2) Claude에게 반영 요청 (Claude Code 프롬프트에 입력)

| 상황 | 입력할 문장 |
|---|---|
| 이미 게시된 편을 고쳤을 때 | `solar-ess 2편 초안 수정했어, 블로그에 다시 반영해줘` |
| 여러 편을 고쳤을 때 | `solar-ess 1~2편 초안 수정했어, 반영해줘` |
| 새 편을 게시할 때 | `solar-ess 3편까지 게시해줘` |
| 자리표시(보강 예정)를 채웠을 때 | `solar-ess 2편 보강 예정 채웠어, 반영해줘` |

Claude가 하는 일 (CLAUDE.md의 **Update** 작업):
1. 수정된 초안과 게시본을 비교해 바뀐 내용을 `docs/blog/posts/...`에 반영
2. 글 front matter에 수정일(`date.updated`) 기록 → 글 상단에 수정일 표시
3. 위키(`wiki/projects/<project>.md`, 개념·교훈)와 `wiki/log.md` 갱신
4. `zensical build --clean`으로 오류 확인
5. 커밋·push 여부를 물어보고 진행

### 3) 직접 확인하고 배포하고 싶을 때 (터미널)

```bash
zensical serve --open                 # 로컬 미리보기 http://localhost:8000 (Ctrl+C로 종료)
zensical build --clean                # "No issues found" 확인

git add raw docs wiki
git commit -m "post: solar-ess 2편 수정"
git push                              # GitHub Actions가 1~2분 안에 자동 배포

gh run watch                          # 배포 진행 상황 보기 (선택)
```

배포 후 바로 반영이 안 보이면 브라우저에서 `⌘ + Shift + R`로 강력 새로고침하세요.

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

## 로컬 실행

```bash
uv tool install zensical==0.0.72
zensical serve --open        # http://localhost:8000
zensical build --clean       # "No issues found" 확인
```

## 게시

```bash
git add -A && git commit -m "post: ..." && git push   # GitHub Actions가 자동 배포
```
