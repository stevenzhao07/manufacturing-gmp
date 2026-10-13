# manufacturing-gmp

> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · Affiliation: MedXpert (medical-device RA & regulatory consultancy) · Pure technical input, no commercial promotion.**

医疗器械生产质量管理规范（GMP）自查工具：2014 版条款框架清单 + 版本差异对照（载入两版条款 JSON 自动 diff）+ 过程确认 IQ/OQ/PQ 检查单生成。服务「2025 修订版 vs 2014 版 GMP 差异研究」与生产现场体系自查。

> **2025 修订版已核实事实（2026-10-12 web 一手）**：新版为国家药监局 **2025 年第 107 号公告**，**2026-11-01 施行**，同时废止 2014 年第 64 号通告；新版共 13 章 84 条，含第十二章「不良事件监测、分析和改进」。2014 年第 64 号系**通告**（非部门规章令）。当前处于新旧交替窗口期，出口企业可继续按 ISO 13485 / QMSR 口径并行准备。

这是 MedXpert 把"医疗 AI 信任"方法论工程化落地的可插拔模块之一——把抽象的合规要求变成一条可重复运行的命令或参考实现。方法论四要素（白话版）：**治理守护者 XCGS** ＝ 为 AI 留下可核验的治理证据；**立法者 A³ Laws** ＝ 给自主系统划权限 / 监督 / 追责三条硬边界；**护照官 AI 护照** ＝ 为模型签发可追溯的身份凭证；**人机共存** ＝ 明确人类与 AI 的分工与兜底。

---

## 可插拔模块契约（lgd-skeleton/1.0）

本仓库是一个 **`lgd-skeleton/1.0` 可插拔模块**：

- **一切即插件**：仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由发现；
- **扩展点**：`plugins/`(新增条款：在 GMP_CHAPTERS 加一项；差异对照只需维护条款 JSON。)。

机器可发现入口：`AGENTS.md` · `CLAUDE.md` · `llms.txt`。

## 特性

- GMP 条款框架清单（2014 版章节结构，2025 修订关注项以 TO_BE_VERIFIED 占位，不虚构条款号）
- 版本差异：--diff old.json new.json 自动比对条款增删改
- IQ/OQ/PQ 三阶段检查单生成（安装/运行/性能确认）
- 零依赖 + CLI

## 内容说明

条款内容以官方发布文本为准；本工具不复制法规全文，只提供结构清单与差异计算能力。2025 修订版具体差异项需按官方通告逐条填入（TO_BE_VERIFIED 占位）。

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

```bash
python scripts/gmp_toolkit.py --demo
python scripts/gmp_toolkit.py --pq
python scripts/gmp_toolkit.py --diff gmp2014.json gmp2025.json
```

> `--diff` 需**自备**两版条款 JSON（按官方通告整理；本仓不随附法规全文）。文件缺失或 JSON 格式错误时工具以退出码 2 报错并提示，不会静默失败。

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/manufacturing-gmp.git && cd manufacturing-gmp
python scripts/gmp_toolkit.py --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/manufacturing-gmp/issues) · 完整《AI 参与指南》见 [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)。

## 路由（总入口）

本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 作为 `lgd-skeleton/1.0` 总入口自动路由发现。

## 关联模块

- [sterilization-validation](https://github.com/stevenzhao07/sterilization-validation)
- [design-controls-toolkit](https://github.com/stevenzhao07/design-controls-toolkit)
- [device-regulatory-map](https://github.com/stevenzhao07/device-regulatory-map)

## 许可

CC-BY-4.0 — 见 [LICENSE](./LICENSE)。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见 `medical-ai-toolkit` 导航
