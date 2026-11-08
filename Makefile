export m

# 사용법
#   make preview              초안 → 블로그 변환 후 로컬 미리보기 (http://localhost:8000)
#   make build                변환 + 빌드 오류 검사만
#   make publish m="메시지"    변환 + 검사 + 커밋 + push (자동 배포)

.PHONY: posts preview build publish

posts:
	@python3 scripts/build_posts.py

preview: posts
	zensical serve --open

build: posts
	@zensical build --clean 2>&1 | tee /dev/stderr | grep -q "No issues found" || (echo "[오류] 빌드 경고/오류를 확인하세요" && exit 1)

publish: build
	git add -A
	@git commit -m "$${m:-post: 블로그 업데이트}" || echo "커밋할 변경이 없습니다"
	git push
	@echo "배포 시작됨 → 1~2분 뒤 https://unity-lin.github.io/ (진행 확인: gh run watch)"
