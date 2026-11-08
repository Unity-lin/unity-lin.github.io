"""블로그용 SVG 차트 생성: python3 make_charts.py (표준 라이브러리만 사용)

데이터 출처: 시뮬레이터 1년 재현(2025년 Open-Meteo 기상 기록, 10분 간격, 10개 지역).
"""
from pathlib import Path

OUT = Path(__file__).parent
FONT = "Pretendard, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
INK, QUIET, GRID, AXIS = "#1f2328", "#656d76", "#e6e8eb", "#8c959f"
ACCENT, MUTED, BAD = "#2f6fdb", "#b8bcc2", "#d1495b"


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}" font-family="{FONT}" font-size="12">'
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>{body}</svg>\n')


def text(x, y, s, size=12, fill=INK, weight=400, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'


def line_chart(name, title, subtitle, xs, xlabel, series, vmax, ystep, unit, notes=(), legend=False):
    """series: [(이름, 색, 굵기, {x: 값})]. notes: [(x, 값, 글, dy)]"""
    left, right, y0, base = 64, 660, 88, 320
    X = lambda x: left + (x - xs[0]) / (xs[-1] - xs[0]) * (right - left)
    Y = lambda v: base - v / vmax * (base - y0)
    b = [text(24, 32, title, 16, weight=600), text(24, 54, subtitle, 12, QUIET)]
    v = 0
    while v <= vmax + 1e-9:
        b.append(f'<line x1="{left}" x2="{right}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{AXIS if v == 0 else GRID}"/>')
        b.append(text(left - 10, Y(v) + 4, f"{v:g}", 11.5, QUIET, anchor="end"))
        v += ystep
    b.append(text(left - 10, y0 - 16, unit, 11.5, QUIET, anchor="end"))
    for x in xs:
        b.append(text(X(x), base + 22, xlabel(x), 11.5, QUIET, anchor="middle"))
    for label, color, width, data in series:
        pts = sorted(data.items())
        d = "".join(f"{'L' if i else 'M'}{X(x):.1f} {Y(v):.1f}" for i, (x, v) in enumerate(pts))
        b.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"/>')
        b += [f'<circle cx="{X(x):.1f}" cy="{Y(v):.1f}" r="3" fill="{color}"/>' for x, v in pts]
        if not legend:  # 선 끝에 이름. 끝점이 겹치면 legend=True로 위쪽 범례
            lx, lv = pts[-1]
            b.append(text(X(lx) + 12, Y(lv) + 4, label, 12, INK, 600))
    if legend:
        lx = right
        for label, color, width, _ in reversed(series):
            lx -= 7 * len(label) + 40
            b.append(f'<line x1="{lx}" x2="{lx + 18}" y1="74" y2="74" stroke="{color}" stroke-width="{width}"/>')
            b.append(text(lx + 24, 78, label, 11.5, QUIET))
    for x, v, s, dy in notes:
        b.append(text(X(x), Y(v) + dy, s, 11.5, INK, 600, "middle"))
    (OUT / name).write_text(svg(760, 352, "".join(b), title), encoding="utf-8")


def bar_chart(name, title, subtitle, rows):
    """rows: [(지역, 가득%, 바닥%)] — 지역별 가로 막대 두 개"""
    left, right, y0, rh = 120, 640, 104, 30
    vmax = 25
    X = lambda v: left + v / vmax * (right - left)
    b = [text(24, 32, title, 16, weight=600), text(24, 54, subtitle, 12, QUIET)]
    b.append(f'<rect x="{left}" y="68" width="12" height="12" fill="{ACCENT}"/>' + text(left + 18, 79, "가득 참 (Full)", 11.5, QUIET))
    b.append(f'<rect x="{left + 130}" y="68" width="12" height="12" fill="{BAD}" fill-opacity="0.75"/>' + text(left + 148, 79, "바닥남 (Empty)", 11.5, QUIET))
    for v in range(0, vmax + 1, 5):
        b.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{y0 - 6}" y2="{y0 + rh * len(rows)}" stroke="{AXIS if v == 0 else GRID}"/>')
        b.append(text(X(v), y0 + rh * len(rows) + 18, f"{v}%", 11.5, QUIET, anchor="middle"))
    for i, (region, full, empty) in enumerate(rows):
        y = y0 + i * rh
        b.append(text(left - 12, y + 16, region, 12.5, INK, anchor="end"))
        b.append(f'<rect x="{left}" y="{y + 3}" width="{X(full) - left:.1f}" height="10" fill="{ACCENT}"/>')
        b.append(text(X(full) + 6, y + 12, f"{full}", 10.5, QUIET))
        if empty:
            b.append(f'<rect x="{left}" y="{y + 15}" width="{max(1.5, X(empty) - left):.1f}" height="10" fill="{BAD}" fill-opacity="0.75"/>')
            b.append(text(X(empty) + 6, y + 24, f"{empty}", 10.5, QUIET))
    h = y0 + rh * len(rows) + 40
    (OUT / name).write_text(svg(760, h, "".join(b), title), encoding="utf-8")


months = list(range(1, 13))
line_chart(
    "monthly-psh-2025.svg",
    "부산은 매달 서울보다 더 발전했고, 두 곳 모두 10월이 가장 낮았다",
    "월별 하루 평균 발전시간(h), 200Wp 장치, 2025년 실측 기상 재현",
    months, lambda m: f"{m}월",
    [("서울", MUTED, 2, dict(zip(months, [2.7, 3.8, 3.8, 3.8, 3.4, 3.4, 3.4, 3.5, 2.9, 2.3, 2.9, 2.5]))),
     ("부산", ACCENT, 2.5, dict(zip(months, [3.9, 4.5, 3.9, 4.5, 4.1, 3.8, 4.5, 4.1, 3.5, 2.9, 3.8, 3.4])))],
    5, 1, "h/일", notes=[(10, 2.9, "2.9h", -12), (10, 2.3, "2.3h", 22)])

hours = list(range(5, 20))
line_chart(
    "fallback-fix-hourly.svg",
    "대체 계산은 아침·저녁 발전을 빠뜨려 실측의 절반만 냈다",
    "시간대별 평균 발전량(W), 10개 지역 1년 평균, 2025년 재현",
    hours, lambda h: f"{h}시",
    [("수정 전 대체 계산", BAD, 2, {5: 0, 6: 0, 7: 1, 8: 8, 9: 21, 10: 38, 11: 58, 12: 69, 13: 60, 14: 41, 15: 23, 16: 9, 17: 2, 18: 0, 19: 0}),
     ("실측 기상", MUTED, 2, {5: 0, 6: 4, 7: 17, 8: 41, 9: 66, 10: 86, 11: 97, 12: 101, 13: 96, 14: 85, 15: 65, 16: 41, 17: 17, 18: 4, 19: 0}),
     ("수정 후 대체 계산", ACCENT, 2.5, {5: 0, 6: 2, 7: 15, 8: 39, 9: 65, 10: 83, 11: 95, 12: 98, 13: 95, 14: 84, 15: 67, 16: 43, 17: 18, 18: 4, 19: 0})],
    120, 20, "W", legend=True)

bar_chart(
    "battery-full-empty.svg",
    "배터리는 1년의 13~20%를 가득 찬 채 보냈고, 바닥난 건 중부뿐이었다",
    "지역별 배터리 상태 비율(%), 1.28kWh LiFePO4, 2025년 실측 기상 재현",
    [("서울", 13.0, 6.8), ("강원 춘천", 14.3, 5.9), ("강원 강릉", 16.4, 2.4), ("대전", 16.9, 1.2), ("전북 전주", 17.2, 0.9),
     ("광주", 18.0, 0.6), ("전남 목포", 19.3, 0.1), ("대구", 18.6, 0.0), ("부산", 19.8, 0.0), ("제주", 16.6, 0.0)])

print("written:", *sorted(p.name for p in OUT.glob("*.svg")))
