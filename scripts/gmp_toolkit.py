#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gmp_toolkit.py — 医疗器械生产质量管理与过程确认工具
====================================================
三块能力：
  1. GMP 条款框架清单（2014 版章节结构；2025 修订版差异 TO_BE_VERIFIED 占位，
     不虚构条款号——差异须按官方通告逐条填入）
  2. 版本差异对照：--diff old.json new.json 自动比对条款增/删/改
  3. 过程确认 IQ/OQ/PQ 三阶段检查单生成

已核实事实（2026-10-12，gov.cn / CFDI）：
  - 现行 2014 版：《医疗器械生产质量管理规范》，国家食品药品监督管理总局
    **2014年第64号通告**发布（注意是**通告/公告**形式，非部门令），共 13 章 84 条。
  - 2025 修订版已正式发布：国家药监局**2025年第107号公告**（2025-11-04 公布），
    **2026-11-01 起施行**，同时废止 2014年第64号通告；第二章"机构与人员"
    改为"质量保证"等结构调整以官方文本为准。
  - 当前（2026-10-12）处于"已发布、即将施行"窗口期。

诚实边界：不复制法规全文；条款内容以官方发布文本为准。
"""
from __future__ import annotations
import argparse
import json
import sys

# 2014 版 GMP（《医疗器械生产质量管理规范》，国家食品药品监督管理总局 2014年第64号
# **通告**发布，共 13 章 84 条）章节框架
# 2025 修订版（国家药监局 2025年第107号公告，2026-11-01 施行）已核实发布，差异项
# 见 REVISION_2025_WATCHLIST（TO_BE_VERIFIED：逐条以官方文本填入）。
GMP_CHAPTERS = [
    ("第一章", "总则", "目的/依据/适用范围/基本原则"),
    ("第二章", "机构与人员", "组织/职责/人员资质/培训/健康管理"),
    ("第三章", "厂房与设施", "选址/洁净车间/环境控制/防虫防鼠"),
    ("第四章", "设备", "配置/维护/校准/状态标识"),
    ("第五章", "文件管理", "质量手册/程序文件/技术文件/记录"),
    ("第六章", "设计开发", "与 ISO 13485 §7.3 衔接"),
    ("第七章", "采购", "供应商/采购信息/进货检验"),
    ("第八章", "生产管理", "指令/过程确认/标识/可追溯"),
    ("第九章", "质量控制", "检验/委托检验/放行"),
    ("第十章", "销售和售后服务", "经销商/售后/客户投诉"),
    ("第十一章", "不合格品控制", "标识/隔离/处置"),
    ("第十二章", "不良事件监测、分析和改进", "不良事件监测/召回/纠正措施/持续改进"),
    ("第十三章", "附则", "术语定义/施行日期/解释权"),
    ("附录", "无菌医疗器械/植入性器械等专项要求", "按产品类别的附加条款"),
]

# 2025 修订版差异关注方向（TO_BE_VERIFIED：须按 2025年第107号公告官方文本逐条核实后填入；
# 2026-11-01 起 2025 版施行并废止 2014 版）
REVISION_2025_WATCHLIST = [
    "数字化/电子记录与电子签名条款（与 21 CFR Part 11 对齐）",
    "UDI 全生命周期贯通（生产→流通→使用）",
    "唯一标识与追溯系统的现场核查要求",
    "委托生产与注册人备案人制度衔接",
    "创新器械/附条件批准的过程控制弹性",
    "章节结构调整（如第二章改『质量保证』——以官方文本为准）",
]

IQOQPQ = [
    ("IQ", "安装确认", [
        "设备/系统按规范到位（位置/环境/公用工程）",
        "随机文件/校准证书/材质证明齐备",
        "操作维护规程初稿完成",
    ]),
    ("OQ", "运行确认", [
        "功能/运行范围挑战（空载）",
        "报警/互锁/权限控制验证",
        "关键工艺参数（CPP）范围确认",
    ]),
    ("PQ", "性能确认", [
        "模拟生产/最差条件负载运行",
        "产品/工艺指标验收（含微生物/内毒素挑战）",
        "取样方案与合格判据（含三次成功惯例，需论证）",
    ]),
]


def diff_versions(old: dict, new: dict) -> dict:
    """old/new: {clause_id: text}。返回增/删/改清单。"""
    old_k, new_k = set(old), set(new)
    added = sorted(new_k - old_k)
    removed = sorted(old_k - new_k)
    changed = sorted(k for k in old_k & new_k if old[k] != new[k])
    return {"added": added, "removed": removed, "changed": changed,
            "summary": f"+{len(added)} / -{len(removed)} / ~{len(changed)}"}


def render_iqoqpq() -> str:
    lines = ["# 过程确认（IQ/OQ/PQ）检查单", "",
             "> 由 gmp_toolkit.py 生成；「三次成功」为行业惯例，须按产品风险论证后采纳。", ""]
    for code, name, items in IQOQPQ:
        lines.append(f"## {code} · {name}")
        for it in items:
            lines.append(f"- [ ] {it}")
        lines.append("")
    return "\n".join(lines)


def _demo() -> int:
    print("GMP 生产质量管理工具 · 演示\n")
    print(f"### 2014 版 GMP 章节框架（{len(GMP_CHAPTERS)} 个）")
    for ch, name, desc in GMP_CHAPTERS:
        print(f"  {ch} {name} — {desc}")
    print("\n### 2025 修订版关注方向（TO_BE_VERIFIED：须按官方通告核实）")
    for w in REVISION_2025_WATCHLIST:
        print(f"  - {w}")
    print("\n### 过程确认（IQ/OQ/PQ）")
    for code, name, items in IQOQPQ:
        print(f"  {code} {name}: {len(items)} 项")
    print("\n[demo] 版本差异: python scripts/gmp_toolkit.py --diff old.json new.json")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="GMP 生产质量与过程确认工具")
    ap.add_argument("--demo", action="store_true", help="跑内置演示")
    ap.add_argument("--chapters", action="store_true", help="打印 GMP 章节框架")
    ap.add_argument("--pq", action="store_true", help="打印 IQ/OQ/PQ 检查单")
    ap.add_argument("--diff", nargs=2, metavar=("OLD", "NEW"),
                    help="比对两个条款 JSON（{clause_id: text}）")
    args = ap.parse_args()

    if args.demo:
        return _demo()
    if args.chapters:
        for ch, name, desc in GMP_CHAPTERS:
            print(f"{ch}\t{name}\t{desc}")
        return 0
    if args.pq:
        print(render_iqoqpq())
        return 0
    if args.diff:
        import os
        for p in args.diff:
            if not os.path.isfile(p):
                print(f"[err] 文件不存在: {p}（--diff 需两个条款 JSON，"
                      f"格式 {{clause_id: text}}；可先从官方文本整理出两版条款 JSON）")
                return 2
        try:
            old = json.load(open(args.diff[0], encoding="utf-8"))
            new = json.load(open(args.diff[1], encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"[err] JSON 解析失败: {exc}（须为 UTF-8 编码的 {{clause_id: text}} 对象）")
            return 2
        d = diff_versions(old, new)
        print(f"差异汇总: {d['summary']}")
        print(f"新增: {d['added'] or '无'}")
        print(f"删除: {d['removed'] or '无'}")
        print(f"修改: {d['changed'] or '无'}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
