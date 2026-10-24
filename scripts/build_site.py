"""Rebuild card previews and the static gallery from repository-local assets."""
import argparse
import hashlib
import html
import json
import os
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/baihejiangnan/gpt-silver-dragon-artwork'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--render-cards', action='store_true', help='Regenerate card PNGs and overviews after changing illustrations or effects')
parser.add_argument('--font', default='C:/Windows/Fonts/msyh.ttc' if os.name == 'nt' else None)
parser.add_argument('--font-bold', default='C:/Windows/Fonts/msyhbd.ttc' if os.name == 'nt' else None)
args = parser.parse_args()
cards = json.loads((ROOT / 'data/common-cards.v1.json').read_text('utf-8'))
old = json.loads((ROOT / 'prompts/experiments.v1.json').read_text('utf-8'))
assert len(cards) == len({c['source_class'] for c in cards}) == 23
assert [c['number'] for c in cards] == list(range(1, 24))
for c in cards:
    assert (ROOT / c['image']).is_file(), c['image']

if args.render_cards:
    from PIL import ImageDraw, ImageFont
    if not args.font or not args.font_bold:
        parser.error('--render-cards requires --font and --font-bold paths to CJK fonts on this OS')
    font = lambda size, strong=False: ImageFont.truetype(args.font_bold if strong else args.font, size)

    def centered(draw, text, y, f, fill, x=300):
        draw.text((x, y), text, font=f, fill=fill, anchor='mt')

    def wrap(text, f, width):
        lines = []
        for paragraph in filter(None, re.split(r'(?<=[。，])', text)):
            line = ''
            for ch in paragraph:
                if f.getlength(line + ch) > width and ch not in '。，；：！？':
                    lines.append(line)
                    line = ch
                else:
                    line += ch
            if line:
                lines.append(line)
        return lines

    previews = []
    for c in cards:
        art = Image.open(ROOT / c['image']).convert('RGB')
        assert art.width * 3 == art.height * 4, f"{c['number']}: illustration must be 4:3"
        card = Image.new('RGB', (600, 900), '#15131e')
        dr = ImageDraw.Draw(card)
        dr.rounded_rectangle((7, 7, 592, 892), 27, fill='#33303f', outline='#b2adbe', width=3)
        dr.rounded_rectangle((17, 17, 582, 882), 20, fill='#201d2b', outline='#615d70', width=2)
        dr.rounded_rectangle((28, 29, 572, 105), 12, fill='#484453')
        centered(dr, c['name'], 48, font(34, True), '#fbf6ff', 326)
        card.paste(art.resize((544, 408), Image.Resampling.LANCZOS), (28, 113))
        dr.rectangle((28, 113, 571, 520), outline='#b2adbe', width=2)
        dr.polygon([(62, 17), (96, 38), (96, 78), (62, 99), (28, 78), (28, 38)], fill='#514665', outline='#ddd2ed', width=3)
        dr.text((62, 58), c['cost'], font=font(40, True), fill='#fff9ff', anchor='mm')
        dr.rounded_rectangle((239, 503, 361, 541), 7, fill='#b9b3c5', outline='#ebe3f4', width=2)
        centered(dr, c['type'], 509, font(23, True), '#272330')
        dr.rounded_rectangle((30, 555, 570, 776), 10, fill='#292533', outline='#554e65', width=1)
        lines = wrap(c['effect'], font(28), 486)
        assert len(lines) <= 5, f"{c['number']}: effect text exceeds card body"
        for i, line in enumerate(lines):
            centered(dr, line, 665 - len(lines) * 42 // 2 + i * 42, font(28), '#f4edf8')
        pending = c['evidence'].startswith('本地')
        flag = '旧版数值参考 · 待核对' if pending else ('消耗范围待核对' if c['number'] == 16 else '基础效果 · 视觉初稿')
        centered(dr, flag, 793, font(20), '#e7bc83' if pending or c['number'] == 16 else '#b7abc8')
        dr.line((39, 831, 561, 831), fill='#595166', width=1)
        dr.text((42, 846), f"{c['number']:02d}  /  {c['rarity']}", font=font(21, True), fill='#d4ccdf')
        dr.text((558, 846), '原牌：' + c['source_name'], font=font(21), fill='#c9c0d3', anchor='rt')
        dest = ROOT / c['preview']
        dest.parent.mkdir(parents=True, exist_ok=True)
        card.save(dest)
        previews.append(card)
    (ROOT / 'overviews').mkdir(exist_ok=True)
    for start in range(0, 23, 6):
        group = cards[start:start + 6]
        sheet = Image.new('RGB', (1896, 1950), '#14111d')
        dr = ImageDraw.Draw(sheet)
        dr.text((30, 22), f"GPT 白银龙娘  /  普通展示组  {start+1:02d}—{start+len(group):02d}", font=font(36, True), fill='#e8e0f1')
        dr.text((32, 77), '23张视觉初稿 · 含3张基础牌 · 金色提示表示规则资料待核对', font=font(23), fill='#b9accd')
        for offset, c in enumerate(group):
            sheet.paste(previews[start + offset], (24 + offset % 3 * 624, 126 + offset // 3 * 912))
        sheet.save(ROOT / f'overviews/overview-{start+1:02d}-{start+len(group):02d}.png')

esc = html.escape
items = []
for c in cards:
    assert (ROOT / c['preview']).is_file(), c['preview']
    num = f"{c['number']:02d}"
    items.append(f'''<article id="card-{num}"><a class="card-image" href="{c['preview']}" target="_blank" rel="noopener"><img src="{c['preview']}" alt="{num} {esc(c['name'])}完整卡面" loading="lazy" width="600" height="900"></a><div class="meta"><h3>{num} · {esc(c['name'])}</h3><p class="source">原牌：{esc(c['source_name'])} · {c['rarity']} · {c['cost']}费 · {c['type']}</p><p>{esc(c['theme'])}</p><details><summary>构图、组合与修改入口</summary><p>{esc(c['art'])}</p><p><b>组合：</b>{esc(c['combo'])}</p><p class="source">{esc(c['evidence'])}；升级效果待同版本资料核对。</p><p><a href="{c['image']}">独立插画原图</a> · <a href="{REPO}/blob/main/prompts/common-cards.v1.json">原始提示词</a> · <a href="{REPO}/issues/new?title={num}%20%E5%8D%A1%E9%9D%A2%E4%BF%AE%E6%94%B9">提修改建议</a></p></details></div></article>''')

characters = []
for file, title in [('01_portrait.png', '脸部特写'), ('02_front.png', '正面全身'), ('03_side.png', '左侧全身'), ('04_back.png', '背面全身'), ('character-sheet-v1.png', '完整四视图资产卡')]:
    characters.append(f'<figure><a href="assets/character/{file}"><img src="assets/character/{file}" alt="{title}" loading="lazy"></a><figcaption>{title} · 点击查看原图</figcaption></figure>')
experiments = []
for c in old['assets']:
    experiments.append(f'<figure><a href="{c["image"]}"><img src="{c["image"]}" alt="{esc(c["title"])}试稿" loading="lazy" width="1448" height="1086"></a><figcaption>{esc(c["title"])}</figcaption></figure>')
archive = ''.join(f'<li><a href="{p.relative_to(ROOT).as_posix()}">{esc(p.name)}</a></li>' for p in sorted((ROOT / 'assets/archive').glob('*.png')))
template = (ROOT / 'scripts/site-template.html').read_text('utf-8')
for key, value in {'CARDS': ''.join(items), 'CHARACTERS': ''.join(characters), 'EXPERIMENTS': ''.join(experiments), 'ARCHIVE': archive, 'REPO': REPO}.items():
    template = template.replace('{{' + key + '}}', value)
assert '{{' not in template
(ROOT / 'index.html').write_text(template, 'utf-8')

assets = []
for p in sorted((ROOT / 'assets').rglob('*.png')):
    with Image.open(p) as image:
        assets.append({'file': p.relative_to(ROOT).as_posix(), 'width': image.width, 'height': image.height, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size})
(ROOT / 'data/assets.json').write_text(json.dumps(assets, ensure_ascii=False, indent=2) + '\n', 'utf-8')
print(f"Built index.html: {len(cards)} cards, 5 character views/sheets, {len(old['assets'])} experiments, {len(assets)} source PNGs")
