# AGENTS.md · manufacturing-gmp

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
医疗器械生产质量管理规范（GMP）自查工具：2014 版条款框架清单 + 版本差异对照（载入两版条款 JSON 自动 diff）+ 过程确认 IQ/OQ/PQ 检查单生成。服务「2025 修订版 vs 2014 版 GMP 差异研究」与生产现场体系自查。

## 运行
```bash
python scripts/gmp_toolkit.py --demo
python scripts/gmp_toolkit.py --help
```

## 扩展契约（lgd-skeleton/1.0）
- **一切即插件**：仅依赖声明式 `module.json`，零配置。
- **按需装（lazy）**：仅 triggers 命中时加载。
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由。
- **扩展点**：`plugins/`(新增条款：在 GMP_CHAPTERS 加一项；差异对照只需维护条款 JSON。)

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作为贡献者署名（@stevenzhao07）。
