---
name: work-report-slides
description: your-slides 系列下的"工作汇报"子技能。把幻灯片改造成让听众能立刻做决策的工作汇报格式 — 周报式、月度复盘式、项目里程碑式、BLUF 向上汇报式。强结论先行、数据指标外露、行动项闭环、责任人明确。当用户说"做汇报""周报 PPT""月度总结""项目复盘""向老板汇报""OKR review""年终总结"或上传内容里包含 KPI、目标完成度、行动项清单、风险/阻塞列表时触发。**每次调用先确认保留策略（默认复制原页再改）、风格三连问、输出设计方案让用户确认，再动手**。支持 HTML / PPTX (Office MCP / 独立生成) / PNG 四种输出格式。
---

# Work Report Slides — 工作汇报叙事

把幻灯片从"罗列工作"改造为"让人能做决策"。

**核心理念**：结论先行（BLUF）→ 数据支撑 → 明确的行动项。听众**不在乎过程，只在乎结论和决策**。

> ℹ️ 这是 `your-slides` 系列的一员，专攻工作汇报。产品发布会见 `launch-slides`，学术交流见 `academic-slides`。

---

## 何时触发

- 用户说"做汇报""周报 PPT""月度总结""项目复盘""向老板汇报""OKR review""年终总结""董事会汇报""跨部门同步"
- 用户调用 `/work-report-slides`
- 用户上传内容里包含 KPI 数字、目标完成度、行动项清单、风险/阻塞、责任人列表
- 用户对一页/几页的吐槽是"看不出结论""老板会问 so what""一堆字没重点"

**不要触发**：
- 产品/项目对外发布、客户演示 → 转 `launch-slides`
- 论文/学术会议/课题汇报 → 转 `academic-slides`
- 纯流程图、纯架构图（信息图优先，不是叙事）

---

## 与发布会、学术的关键差异

| 维度 | launch-slides | academic-slides | work-report-slides |
|---|---|---|---|
| 听众心理 | 想被打动 | 想被说服 | 想做决策 |
| 信息密度 | 极低，留白多 | 高 | 中-高，但要分层 |
| 第一眼看到 | 金句/宣言 | 章节标题 | **结论 + 状态灯** |
| 关键页 | 价值总结 | 方法/结果 | 行动项 + 风险 |
| 容忍冗余 | 不容忍 | 适度容忍 | **零容忍**（老板时间贵） |
| 数字呈现 | 大字号孤立 | 表格+置信区间 | 状态灯 + 偏差归因 |

---

## 必读文件清单（按顺序）

执行任务前按顺序读完相关文件，**不要凭记忆做事**：

| 步骤 | 文件 | 何时读 |
|---|---|---|
| 1 | [workflow/interaction-protocol.md](workflow/interaction-protocol.md) | 每次调用必读，6 步流程 |
| 2 | [workflow/design-plan-template.md](workflow/design-plan-template.md) | 风格三连问之后，输出设计方案前 |
| 3 | [styles/](styles/) 下对应风格的 `.md` | 用户确认风格之后 |
| 4 | [formats/](formats/) 下对应输出格式的 `.md` | 用户在设计方案里选完输出格式之后 |
| 5 | [workflow/anti-patterns.md](workflow/anti-patterns.md) | 自检阶段必过 |

---

## 核心约束（继承 your-slides 系列，违反任一条算失败）

### 约束 1 — 保留策略每次必问

修改前必须问："复制当前页再改 / 直接改 / 新建一页"，**默认"复制再改"**。

工作汇报场景尤其重要：老板/同事经常在你改完后说"还是上版本的某个图好"，没有副本就回不去了。详细模板见 [workflow/interaction-protocol.md](workflow/interaction-protocol.md) Step 0。

### 约束 2 — 设计方案先于生成

用户没看过文字版方案，**禁止动手生成页面**。

工作汇报的"方案"长这样：**BLUF（一句结论） + 3-5 个支撑指标 + 行动项 + 责任人**。输出格式见 [workflow/design-plan-template.md](workflow/design-plan-template.md)。

### 约束 3 — 输出格式必须用户选

工作汇报最常见是 PPTX（直接发会议群/邮件），但也有用户想要 HTML 当看板用。4 种格式：

- **HTML 单文件** — Claude 直接生成，无外部依赖；适合做"活看板"
- **PPTX via Office MCP** — 在用户已打开的 PowerPoint 里实时改；适合周会/月会现场调整
- **PPTX 独立生成** — 通过 `pptx` 技能离线生成；适合发邮件归档
- **图片 PNG** — 截图或 SVG；适合发 IM 群同步、嵌入 Notion/飞书文档

限制条件见 [formats/](formats/) 下对应文件。

---

## 6 步流程（高层）

详见 [workflow/interaction-protocol.md](workflow/interaction-protocol.md)：

```
Step 0  保留策略（默认复制再改）             ← 必问,约束 1
Step 1  识别意图（单页重做/新建/多页汇报序列）
Step 2  风格三连问（Q1 风格 + Q2 听众层级 + Q3 状态灯口径）
Step 3  输出 BLUF + 指标 + 行动项方案         ← 必做,约束 2
Step 4  按用户选的输出格式执行
Step 5  验证 + 用户最终确认
```

---

## 4 种汇报风格速览

详细布局、配色、字号见 [styles/](styles/)：

| 风格 | 文件 | 一句话特征 |
|---|---|---|
| 周报式 | [styles/weekly-status.md](styles/weekly-status.md) | 三栏固定（上周 Done / 本周 Plan / 风险） + 总状态灯 |
| 月度复盘式 | [styles/monthly-review.md](styles/monthly-review.md) | 目标 vs 实际表格 + 状态灯 + 偏差归因 + 下月动作 |
| 项目里程碑式 | [styles/project-milestone.md](styles/project-milestone.md) | 横向 timeline + 完成/进行/未来标记 + 当前风险 |
| BLUF 向上汇报式 | [styles/bluf-up-pitch.md](styles/bluf-up-pitch.md) | 一句结论占顶 + 3 支撑要点 + 明确的 ask |

---

## 状态灯统一规范（跨所有风格）

工作汇报最容易出问题的地方就是**状态灯口径不一致**。统一约定：

| 状态 | 颜色 | 圆点 | 含义 |
|---|---|---|---|
| 🟢 绿（On Track） | `#22C55E` | ●  | 进展符合预期，无需关注 |
| 🟡 黄（At Risk） | `#F59E0B` | ●  | 有风险但可控，需要关注 |
| 🔴 红（Off Track） | `#EF4444` | ●  | 已偏离目标或被阻塞，需要决策/资源 |
| ⚪ 灰（Not Started / Done） | `#94A3B8` | ●  | 未开始或已完成（关闭态） |

⚠️ **不要发明新颜色**（紫色"特别紧急"、蓝色"待评估"等）——多色会让听众停下来想含义，破坏决策效率。

---

## 字号锚点（跨风格通用）

| 元素 | 字号 | 用途 |
|---|---|---|
| 页面标题 | 24-28pt | "2026 W18 周报"等 |
| BLUF 结论句 | 28-36pt | 一句话总结 |
| 关键 KPI 数字 | 32-48pt | 比较显眼但不像发布会那么夸张 |
| 二级标题（栏目名） | 16-18pt | "上周完成 / 本周计划"等 |
| 正文 bullet | 12-14pt | 细节 |
| 责任人/时间标签 | 10-11pt | @张三 / 2026-W19 |

⚠️ 工作汇报字号比发布会**整体小一档**，因为信息密度更高，且听众通常是近距离看屏幕/打印件，不是远距离看大屏。

---

## 反模式（每次完成前自检，完整清单见 [workflow/anti-patterns.md](workflow/anti-patterns.md)）

5 条最常踩的：

- ❌ 罗列工作不写结论 → ✅ 第一句必须是"上周关键结论是 X"
- ❌ 状态灯只有颜色没有归因 → ✅ 黄/红状态必须配一行"为什么 + 我需要的支持"
- ❌ 行动项没有责任人/deadline → ✅ "@张三 W19 内完成" 才算合格
- ❌ 跳过保留策略问询 → ✅ Step 0 必问
- ❌ 跳过 BLUF 方案确认 → ✅ 用户说"可以"才动手
