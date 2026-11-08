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

자세한 규칙은 [CLAUDE.md](CLAUDE.md)에 있습니다.

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
