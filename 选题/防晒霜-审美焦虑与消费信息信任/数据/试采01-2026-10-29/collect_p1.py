#!/usr/bin/env python3
# 试采01 解析脚本：苏宁搜索页(防晒霜)静态 HTML → 商品 CSV + 价格合并
# 用法：python3 collect_p1.py  （在本目录下，需先有 raw-suning-p1.html）
# 价格来源：2026-10-29 浏览器渲染采集（接口路线被拒，见试采记录.md），此处内嵌快照
import re, csv

def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

PRICES = {  # product_id -> 页面价格原文（浏览器渲染快照 2026-10-29）
'12381529123':'¥49.68到手价','12441293414':'¥26.01到手价','11055085890':'¥176.00',
'12450932956':'¥26.01到手价','12379388477':'¥70.31到手价','12447643218':'¥35.91到手价',
'12447546309':'¥245.00到手价','12453398015':'¥255.00到手价','12430628851':'¥269.00到手价',
'12430383214':'¥269.00到手价','12453665226':'¥128.53','12403119726':'',
'11670500981':'¥72.16到手价','12446203558':'¥129.00','12105734259':'¥90.00',
'11840261015':'¥95.00','12365384560':'¥39.90','12105734258':'¥48.00',
'12450932870':'¥15.21到手价','12430312998':'¥85.00','12446162119':'¥245.00到手价',
'12431684020':'¥269.00到手价','12112755533':'¥49.00','683575538':'¥119.00',
'11848523507':'¥189.00','12447723138':'¥13.50到手价','11848699018':'¥79.80',
'12432958643':'¥44.10到手价','12430257721':'¥108.00','11848698942':'¥41.50'}

h = open('raw-suning-p1.html', encoding='utf-8', errors='ignore').read()
items = {}
for b in re.split(r'<div class="res-info">', h)[1:]:
    seg = b[:3000]
    link = re.search(r'href="(//product\.suning\.com/[^"#]+\.html)"', seg)
    if not link:
        continue
    mt = re.search(r'<a[^>]*target="_blank"[^>]*href="//product\.suning\.com[^>]*>(.*?)</a>', seg, re.S)
    msell = re.search(r'<em[^>]*>([^<]+)</em>', seg)
    meval = re.search(r'<i>([^<]+)</i>评价', seg)
    mshop = re.search(r'<a title="([^"]*)"[^>]*class="store-class[^"]*">([^<]*)</a>', seg)
    url = 'https:' + link.group(1)
    pid = url.rstrip('.html').split('/')[-1]
    txt = (strip_tags(mt.group(1)) if mt else '') + ' ' + (strip_tags(msell.group(1)) if msell else '')
    items[pid] = dict(
        product_id=pid, title=strip_tags(mt.group(1)) if mt else '',
        selling_point=strip_tags(msell.group(1)) if msell else '',
        spf_claim=(re.search(r'SPF\s?\d*\+?', txt) or [None]) and (re.search(r'SPF\s?\d*\+?', txt).group(0).replace(' ', '') if re.search(r'SPF\s?\d*\+?', txt) else ''),
        pa_claim=(re.search(r'PA\+{2,4}', txt).group(0) if re.search(r'PA\+{2,4}', txt) else ''),
        evaluate_count=meval.group(1) if meval else '',
        shop_name=(mshop.group(2) or mshop.group(1)) if mshop else '', url=url)

with open('products_pilot01_sunng.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['product_id','title','selling_point','spf_claim','pa_claim','price_cny','price_type','price_raw','shop_name','evaluate_count','url','source','captured_at'])
    for v in items.values():
        raw = PRICES.get(v['product_id'], '')
        m = re.search(r'([\d.]+)', raw)
        w.writerow([v['product_id'], v['title'], v['selling_point'], v['spf_claim'], v['pa_claim'],
                    m.group(1) if m else '', '到手价' if '到手' in raw else ('标价' if raw else '未取到'),
                    raw, v['shop_name'], v['evaluate_count'], v['url'], '苏宁搜索页-防晒霜', '2026-10-29 16:00'])
print(f'OK: {len(items)} rows -> products_pilot01_sunng.csv')
