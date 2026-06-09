---
name: launch-slides
description: your-slides 系列下的"产品发布会"子技能。把幻灯片改造成产品发布会叙事风格 — 苹果式克制、华为/小米式气势、特斯拉式数据墙、或故事弧线式。用于价值总结页、单页重做、或一整套发布会页面。**每次调用先确认保留策略（默认复制原页再改）、风格三连问、输出设计方案让用户确认，再动手**。支持 HTML / PPTX (Office MCP / 独立生成) / PNG 四种输出格式。
---

# Launch Slides — 产品发布会叙事

把幻灯片从"功能罗列"改造为"发布会叙事"。

**核心理念**：一句金句立住主张 → 价值递进 → 留白与节奏。

> ℹ️ 这是 `your-slides` 系列的一员，专攻发布会场景。学术交流见 `academic-slides`，工作汇报见 `work-report-slides`。

---

## 何时触发

- 用户说"把这页改成发布会风格""用 keynote 的感觉重做""价值总结页""产品价值页""看着像功能堆砌帮我重新讲"
- 用户调用 `/launch-slides`
- 用户对一页/几页的吐槽是"平铺直叙""不够有感染力""像 PRD 而不像 keynote"

**不要触发**：
- 纯数据可视化、纯流程图、纯表格页（信息密度优先，不适合发布会叙事）
- 学术答辩、论文汇报 → 转 `academic-slides`
- 周报、月报、向上汇报 → 转 `work-report-slides`

---

## 必读文件清单（按顺序）

执行任务前，按这个顺序读完相关文件，**不要凭记忆做事**：

| 步骤 | 文件 | 何时读 |
|---|---|---|
| 1 | [workflow/interaction-protocol.md](workflow/interaction-protocol.md) | 每次调用必读，里面是 6 步固定流程 |
| 2 | [workflow/design-plan-template.md](workflow/design-plan-template.md) | 用户回答完风格三连问后，输出设计方案前 |
| 3 | [styles/](styles/) 下对应风格的 `.md` | 用户确认风格之后，开始画页面前 |
| 4 | [formats/](formats/) 下对应输出格式的 `.md` | 用户在设计方案里选完输出格式之后 |
| 5 | [workflow/anti-patterns.md](workflow/anti-patterns.md) | 自检阶段，每次完成前过一遍 |

---

## 核心约束（违反任何一条都算失败）

### 约束 1 — 保留策略每次必问

修改前必须问："复制当前页再改 / 直接改 / 新建一页"，**默认选项是"复制再改"**。

为什么：发布会改造是破坏性较强的操作，用户经常想回退对比，但 PPT 撤销栈不稳定。保留副本是最低成本的安全网。

详细提问模板见 [workflow/interaction-protocol.md](workflow/interaction-protocol.md) Step 0。

### 约束 2 — 设计方案先于生成

用户没看过文字版设计方案，**禁止动手生成页面**（无论目标格式是 HTML、PPTX 还是 PNG）。

为什么：生成动作比改文字方案贵 10 倍以上。让用户在最便宜的层面反复迭代到满意，再花贵的步骤。

设计方案的输出格式见 [workflow/design-plan-template.md](workflow/design-plan-template.md)。

### 约束 3 — 输出格式必须用户选

不要默认丢一个 PPTX 给只想要 HTML 预览的用户。在设计方案里明确列出 4 种格式让用户挑：

- **HTML 单文件** — Claude 直接生成，无外部依赖
- **PPTX via Office MCP** — 在用户已打开的 PowerPoint 里实时改，需要 Office MCP 连接
- **PPTX 独立生成** — 通过 `pptx` 技能离线生成新 .pptx 文件，无需 MCP
- **图片 PNG** — 截图或 SVG 路径，部分场景需要 Chrome MCP

每种格式的能力边界和限制见 [formats/](formats/) 下的对应文件。

---

## 6 步流程（高层）

详见 [workflow/interaction-protocol.md](workflow/interaction-protocol.md)。这里只列骨架：

```
Step 0  保留策略（默认复制再改）             ← 必问，约束 1
Step 1  识别意图（单页重做/新建/多页序列）
Step 2  风格三连问（Q1 风格 + Q2 措辞 + Q3 背景，多页加 Q4）
Step 3  输出设计方案 + 等用户说"可以开始"     ← 必做,约束 2
Step 4  按用户选的输出格式执行(读 formats/*.md)
Step 5  验证 + 用户最终确认
```

---

## 4 种叙事风格速览

详细布局图、配色、字号见 [styles/](styles/) 下对应文件：

| 风格 | 文件 | 一句话特征 |
|---|---|---|
| 苹果式·克制留白 | [styles/apple-restrained.md](styles/apple-restrained.md) | 巨幅金句 + 大量黑色留白 + 单行价值点 |
| 华为/小米式·气势递进 | [styles/huawei-momentum.md](styles/huawei-momentum.md) | 顶部主张 + Before/After + 底部数字墙 |
| 特斯拉式·一句话+数据墙 | [styles/tesla-data-wall.md](styles/tesla-data-wall.md) | 颠覆性宣言占中央 + 4 个关键数字 |
| 故事弧线式 | [styles/story-arc.md](styles/story-arc.md) | 痛点→转折→解法→价值 横向时间线 |

---

## 字号锚点速查（跨风格通用）

| 元素 | 字号 | 用途 |
|---|---|---|
| 巨幅金句（苹果/华为） | 44-56pt | 主张 |
| 颠覆宣言（特斯拉） | 56-72pt | 单句中心 |
| 大数字（数据墙） | 48-72pt | 证据 |
| 价值点短语 | 18-24pt | 4 个并列短语 |
| 注解一行话 | 12-14pt | 短语下面的人话 |
| 顶部 tag / 底部 slogan | 11-14pt | 框架文字 |
| 标题栏（模板继承） | 16pt | 不喧宾夺主 |

⚠️ 上述字号是发布会叙事专用，因为页面信息密度极低、留白多，所以小字号也读得清。这与"普通幻灯片 ≥14pt 底线"是不同上下文。

---

## 反模式（每次完成前自检）

完整清单见 [workflow/anti-patterns.md](workflow/anti-patterns.md)。重点 5 条：

- ❌ 价值点术语堆砌（"全链路闭环"）→ ✅ 用动词或对抗短语（"穿透工序"）
- ❌ 金句超 20 字 / 跨两行以上 → ✅ ≤20 字，一口气念完
- ❌ 4 个价值点做成"卡片底色 + 图标 + 三行" → ✅ 序号 + 短语 + 一行注解，无卡片
- ❌ 跳过保留策略问询 → ✅ Step 0 必问，默认复制
- ❌ 跳过设计方案确认 → ✅ 用户说"可以开始"才动手
