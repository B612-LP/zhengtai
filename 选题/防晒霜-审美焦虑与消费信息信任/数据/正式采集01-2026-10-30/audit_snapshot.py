"""只读复核现有真实商品快照，不采集、不改写原始数据。

运行：python3 本文件路径 [--output 核验结果.json]
仅使用 Python 标准库；不执行模拟问卷生成器。
"""
import argparse
import csv
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
BANDS = ["0-50", "50-100", "100-200", "200+"]
SHOPS = ["专营店", "品牌旗舰", "海外专营", "苏宁自营"]


def audit(base=BASE):
    with (base / "products_clean.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    raw = json.loads((base / "products_raw_browser.json").read_text(encoding="utf-8"))
    saved = json.loads((base / "stats_real.json").read_text(encoding="utf-8"))
    errors = []
    raw_ids = [re.search(r"/(\d+)\.html", row["url"]).group(1) for row in raw["rows"]]
    ids = [r["product_id"] for r in rows]
    if len(set(ids)) != len(ids) or set(raw_ids) != set(ids):
        errors.append("原始数据与清洗数据的商品ID集合不一致或清洗表重复")
    if any(r["data_flag"] != "真实公开数据-苏宁搜索页" for r in rows):
        errors.append("真实数据标识异常")
    prices = [float(r["price_cny"]) for r in rows]
    if not prices or not all(math.isfinite(p) and p > 0 for p in prices):
        raise ValueError("价格必须为有限正数")
    expected_band = lambda p: "0-50" if p <= 50 else "50-100" if p <= 100 else "100-200" if p <= 200 else "200+"
    if any(r["price_band"] != expected_band(float(r["price_cny"])) for r in rows):
        errors.append("价格带字段与价格不一致")
    n = len(rows)
    bands = Counter(r["price_band"] for r in rows)
    shops = Counter(r["shop_type"] for r in rows)
    table = {b: {s: sum(r["price_band"] == b and r["shop_type"] == s for r in rows) for s in SHOPS} for b in BANDS}
    expected = [bands[b] * shops[s] / n for b in BANDS for s in SHOPS]
    chi = sum((table[b][s] - bands[b] * shops[s] / n) ** 2 / (bands[b] * shops[s] / n) for b in BANDS for s in SHOPS)
    claims = {kw: sum(kw in r["title"] for r in rows) for kw in saved["claims"]}
    # 使用字面出现率；不将未出现解释为产品不具有相应参数或功效。
    spf50 = sum("SPF50" in r["title"].replace(" ", "").upper() for r in rows)
    pa4 = sum("PA++++" in r["title"].upper() for r in rows)
    result = {
        "data_scope": "2026-10-30苏宁防晒霜搜索快照；非概率商品样本；非市场总体",
        "raw_rows": len(raw["rows"]), "unique_product_ids": n,
        "duplicate_raw_rows": len(raw_ids) - len(set(raw_ids)),
        "price_median": statistics.median(prices), "price_mean": round(statistics.mean(prices), 1),
        "price_std": round(statistics.stdev(prices), 1), "price_min": min(prices), "price_max": max(prices),
        "price_types": dict(Counter(r["price_type"] for r in rows)),
        "bands": {b: bands[b] for b in BANDS}, "claims": claims, "spf50": spf50, "pa4": pa4,
        "cross_band_shop": {"table": table, "chi2": round(chi, 1), "df": 9,
            "cramers_v": round(math.sqrt(chi / (n * 3)), 3),
            "expected_below_5": sum(e < 5 for e in expected), "expected_cells": len(expected),
            "expected_min": round(min(expected), 3),
            "inference_warning": "稀疏单元格；不直接使用渐近卡方p值作确认性推断；样本亦非随机抽样"},
        "shop_price_medians": {s: statistics.median(float(r["price_cny"]) for r in rows if r["shop_type"] == s) for s in SHOPS},
        "limits": ["小样、套装、净含量未统一，不是单位容量价格比较", "到手价与标价混合", "店铺类型由名称规则推断，非平台认证标签", "评价数非销量或产品质量", "商品标题不能代表详情页、注册信息或社媒内容"],
    }
    for key in ["n", "price_median", "price_mean", "price_std", "price_min", "price_max", "bands", "claims", "spf50", "pa4"]:
        actual = n if key == "n" else result[key]
        if saved[key] != actual:
            errors.append(f"与既有stats_real不一致：{key}")
    for key in ["table", "chi2", "df", "cramers_v"]:
        if saved["cross_band_shop"][key] != result["cross_band_shop"][key]:
            errors.append(f"与既有交叉表不一致：{key}")
    result["checks_passed"] = not errors
    result["errors"] = errors
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="可选：写入新的复核摘要；拒绝覆盖任何已有文件")
    args = parser.parse_args()
    result = audit()
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        try:
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(text + "\n")
        except FileExistsError:
            parser.error("输出文件已存在；为保护原始数据，拒绝覆盖，请选择新路径")
    print(text)
    raise SystemExit(0 if result["checks_passed"] else 1)


if __name__ == "__main__":
    main()
