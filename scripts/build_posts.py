#!/usr/bin/env python3
"""raw/<project>/drafts 의 초안을 docs/blog/posts/series/ 아래 블로그 글로 변환한다.

사용법:  python3 scripts/build_posts.py
설정:    raw/<project>/series.toml  (어떤 편을 언제 공개할지)
출력:    docs/blog/posts/series/<project>/<slug>/index.md  (매번 새로 생성, git에 올리지 않음)
"""
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
OUT = ROOT / "docs" / "blog" / "posts" / "series"

PLACEHOLDER = re.compile(r"`\[ (.+?) \]`")          # `[ 조립 사진 ]`
MD_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+\.md)\)")  # [텍스트](02-xxx.md)
IMAGE = re.compile(r"!\[[^\]]*\]\((images/[^)\s]+)\)")


def fail(msg):
    sys.exit(f"[오류] {msg}")


def last_commit_date(path):
    """초안 파일을 마지막으로 커밋한 날짜(YYYY-MM-DD). git 기록이 없으면 None."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        return out or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def front_matter(post, category, updated):
    created = post["date"]
    if updated and updated > created[:10]:
        date = f"date:\n  created: {created}\n  updated: {updated}"
    else:
        date = f"date: {created}"
    return f"---\n{date}\nslug: {post['slug']}\ncategories:\n  - {category}\n---\n\n"


def insert_more(body):
    """제목 다음 첫 문단 뒤에 <!-- more --> (목록 페이지에 보일 요약 경계)."""
    if "<!-- more -->" in body:
        return body
    lines = body.split("\n")
    i = 0
    while i < len(lines) and (not lines[i].strip() or lines[i].startswith("# ")):
        i += 1
    while i < len(lines) and lines[i].strip():
        i += 1
    return "\n".join(lines[:i] + ["", "<!-- more -->"] + lines[i:])


def add_appendix(body, text, title):
    indented = "\n".join(("    " + l) if l.strip() else "" for l in text.strip().split("\n"))
    block = f'??? note "{title}"\n\n{indented}\n'
    lines = body.rstrip().split("\n")
    # 맨 아래 이전/다음 링크(---) 앞에 넣는다
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "---":
            return "\n".join(lines[:i]) + "\n\n" + block + "\n" + "\n".join(lines[i:]) + "\n"
    return body.rstrip() + "\n\n" + block


def build_project(project_dir):
    cfg_path = project_dir / "series.toml"
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
    category = cfg.get("category") or fail(f"{cfg_path}: category 가 없습니다")
    drafts = project_dir / "drafts"
    posts = cfg.get("posts", [])

    published = {p["file"]: p for p in posts if p.get("publish")}
    for p in published.values():
        if not p.get("date"):
            fail(f"{cfg_path}: '{p['file']}' 는 publish = true 인데 date 가 비어 있습니다")
        if not (drafts / p["file"]).exists():
            fail(f"{cfg_path}: 초안 '{drafts / p['file']}' 이 없습니다")

    out_dir = OUT / project_dir.name
    count = 0
    for p in published.values():
        src = drafts / p["file"]
        body = src.read_text(encoding="utf-8")

        def link(m):
            text, target = m.group(1), m.group(2)
            if target in published:
                return f"[{text}](../{published[target]['slug']}/index.md)"
            if (drafts / target).exists():
                return f"{text} *(공개 예정)*"
            return m.group(0)

        body = MD_LINK.sub(link, body)
        body = PLACEHOLDER.sub(r'<span class="todo">보강 예정: \1</span>', body)
        body = insert_more(body)
        if p.get("appendix"):
            extra = (drafts / p["appendix"]).read_text(encoding="utf-8")
            body = add_appendix(body, extra, p.get("appendix_title", "부록"))

        dest = out_dir / p["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        for img in IMAGE.findall(body):
            src_img = project_dir / img
            if not src_img.exists():
                fail(f"{src}: 이미지 '{src_img}' 가 없습니다")
            (dest / img).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_img, dest / img)

        updated = last_commit_date(src)
        (dest / "index.md").write_text(front_matter(p, category, updated) + body, encoding="utf-8")
        count += 1
        print(f"  ✓ {project_dir.name}/{p['file']} → /blog/{p['slug']}/")
    return count


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    total = 0
    for project_dir in sorted(RAW.iterdir()):
        if (project_dir / "series.toml").exists():
            total += build_project(project_dir)
    print(f"블로그 글 {total}편 생성 완료")


if __name__ == "__main__":
    main()
