---
name: figma-pixel-perfect
description: >
  Figma 像素级还原技能 v2。通过 TalkToFigma MCP 读取 Figma 设计数据，
  先分析现有代码库（技术栈、组件、Token），再执行 Gap Analysis 对比设计 vs 代码，
  然后生成高保真前端代码，并通过浏览器验证引擎进行像素级对比校验。
  新增 Plan 生成模式：可按步骤引导输出完整的像素级还原实施计划。
  支持 React/Vue/HTML + Tailwind/CSS Modules。
  Trigger when: 用户需要将 Figma 设计稿转换为前端代码、需要像素级还原设计、
  需要从 Figma 生成组件代码、需要验证前端代码与设计稿的一致性、
  需要生成 Figma 还原 Plan、需要分析现有代码与 Figma 设计的差距、
  需要验证现有 Token 与 Figma 设计的一致性。
license: MIT
metadata:
  author: SOLO Custom Skill
  version: 2.0.0
  mcp_dependencies:
    - TalkToFigma (cursor-talk-to-figma-mcp)
    - integrated_browser
---

# Figma 像素级还原技能 (figma-pixel-perfect) v2.0.0

通过 TalkToFigma MCP 读取 Figma 设计数据，先分析现有代码库，再执行 Gap Analysis 对比设计 vs 代码，然后生成高保真前端代码，并通过浏览器验证引擎进行像素级对比校验。支持 Plan 生成模式，可在代码生成前输出完整的实施计划。

## 核心架构

```
Figma 设计稿
     ↓
[TalkToFigma MCP] ─── 读取设计数据（节点、样式、布局）
     ↓
[代码库分析] ─── 读取 package.json / 目录结构 / 现有组件 / Token / 路由
     ↓
[设计数据采集] ─── 节点 / 样式 / 资产清单 / 精确布局尺寸
     ↓
[Figma 解释引擎] ─── 噪音过滤 + 结构修正 + 语义理解
     ↓
[设计 Token 提取] ─── 颜色/字体/间距/圆角/阴影精确提取
     ↓
[Token 复用验证] ─── 对比 Figma Token vs 现有 Token（Validate, Don't Rebuild）
     ↓
[Gap Analysis] ─── 设计 vs 代码 → ✅/⚠️/❌ 状态标记
     ↓
[代码生成] ─── 按 Gap Analysis 结果决定新建/修改/验证策略
     ↓
[交互状态规划] ─── hover/active/focus/disabled/transition
     ↓
[浏览器验证引擎] ─── 渲染 + DOM/CSS 对比 + 像素级校验
     ↓
[自动修复] ─── 发现偏差后迭代修正
     ↓
最终交付代码
```

## 必需工作流（Required Flow）

### Phase 0: 快速连接（失败再提示，不预先询问）

> **原则：TalkToFigma 无需 Token 验证。先 join_channel，成功后再读取数据。失败则提示用户，绝不跳过 join_channel 直接调用其他 TalkToFigma 工具。**

**⚠️ 强制规则：在 `join_channel` 返回成功之前，禁止调用任何其他 TalkToFigma 工具（get_document_info、get_selection、read_my_design 等）。违反此规则会导致 "Must join a channel before sending commands" 错误并陷入死循环。**

**步骤 0.1: 连接频道（必须第一个执行）**

1. 向用户获取 Channel ID（如果用户未提供，询问一次）
2. 调用 `join_channel(channel: "用户提供的Channel ID")`
3. **判断返回结果：**
   - ✅ **成功** → 进入步骤 0.2
   - ❌ **失败** → 进入步骤 0.3，**到此为止，不要继续调用任何 TalkToFigma 工具**

**步骤 0.2: 验证连接（仅在 join_channel 成功后执行）**

调用 `get_document_info()` 验证通信正常：
- ✅ **返回了文档信息** → 连接成功，直接进入 Phase 1
- ❌ **报错或返回空** → 进入步骤 0.3

**步骤 0.3: 错误处理（仅在连接失败时执行）**

根据错误信息，给用户**一句话提示**，然后**停止**，等待用户回复：

| 错误信息关键词 | 提示用户 |
|---|---|
| `Must join a channel` / `not connected` | "TalkToFigma 连接失败，请确认 WebSocket 服务器已启动（`cd cursor-talk-to-figma-mcp && bun socket`），Figma 插件已运行，Channel ID 正确" |
| 连接超时 / 拒绝连接 | "WebSocket 连接超时，请确认 TalkToFigma WebSocket 服务器正在运行" |
| Channel 不存在 / 无响应 | "Channel ID 无效，请确认 Figma 插件面板中显示的 Channel ID" |
| 返回空数据 / 无选区 | "连接成功但未读取到数据，请在 Figma 中选中目标设计节点后告诉我" |

> **关键：提示后立即停止，不要重试、不要循环、不要调用其他工具。等用户回复后再重新从步骤 0.1 开始。**

---

### Phase 1: 代码库分析

> **目的：在动手写代码之前，先彻底理解现有项目的结构、技术栈、组件体系和 Token 系统。**
> **详见 `references/codebase-analysis.md`**

**步骤 1.1: 读取 package.json → 提取技术栈信息**

读取项目根目录的 `package.json`，提取以下关键信息：

| 字段 | 提取内容 | 示例 |
|---|---|---|
| dependencies | 框架（react/vue/next/nuxt）、组件库（@mui/material/antd）、CSS方案（tailwindcss/styled-components）、图标库（@heroicons/lucide-react） | `"react": "^18.2.0"` |
| devDependencies | TypeScript 版本、构建工具（vite/webpack/turbopack）、测试框架 | `"typescript": "^5.3.0"` |
| scripts | 可用命令（dev/build/lint/test） | `"dev": "next dev"` |

**输出格式 — 技术栈表格：**

```
| 类别 | 技术 | 版本 |
|---|---|---|
| 框架 | React | 18.2.0 |
| 元框架 | Next.js | 14.1.0 |
| 样式方案 | Tailwind CSS | 3.4.1 |
| 组件库 | 自定义组件 | - |
| TypeScript | 是 | 5.3.0 |
| 图标库 | Lucide React | 0.344.0 |
| 构建工具 | Turbopack | - |
```

**步骤 1.2: 扫描目录结构 → 识别项目架构**

使用 Glob 工具扫描项目根目录和 `src/` 目录，识别以下目录：

| 目录模式 | 含义 |
|---|---|
| `src/components/**` | 组件目录 |
| `src/pages/**` 或 `src/app/**` | 页面目录 |
| `src/styles/**` 或 `src/assets/styles/**` | 样式目录 |
| `src/assets/**` | 静态资源目录 |
| `src/types/**` 或 `src/interfaces/**` | 类型定义目录 |
| `src/hooks/**` | 自定义 Hooks |
| `src/utils/**` 或 `src/lib/**` | 工具函数 |
| `src/store/**` 或 `src/context/**` | 状态管理 |
| `src/modals/**` | 弹窗组件 |
| `public/**` | 公共静态资源 |

**步骤 1.3: 读取现有组件 → 列出组件清单**

扫描 `src/components/` 目录下的所有文件，列出每个组件的：
- 文件路径
- 组件名称（从 export default 或命名导出推断）
- 职责描述（从文件名和代码注释推断）
- Props 接口概要

**输出格式 — 组件架构树：**

```
src/components/
├── ui/                          # 基础 UI 组件
│   ├── Button.tsx               # 通用按钮组件
│   ├── Input.tsx                # 输入框组件
│   └── Modal.tsx                # 弹窗组件
├── layout/                      # 布局组件
│   ├── Header.tsx               # 页面头部
│   ├── Sidebar.tsx              # 侧边栏
│   └── Footer.tsx               # 页脚
├── features/                    # 业务功能组件
│   ├── Dashboard/
│   └── Settings/
└── shared/                      # 共享组件
```

**步骤 1.4: 读取现有 Token → 提取设计系统**

查找并读取以下文件（按优先级排序）：

1. `src/**/figmaDesignTokens.ts` — Figma 设计 Token 文件（最高优先级）
2. `src/**/theme.ts` — 主题配置文件
3. `src/**/tokens.ts` — Token 定义文件
4. `tailwind.config.ts` 或 `tailwind.config.js` — Tailwind 配置
5. `src/**/*.css` 中的 `:root` CSS 变量定义

提取内容：
- 颜色 Token（primary/secondary/success/warning/error/neutral）
- 字体 Token（font-family/font-size/font-weight/line-height）
- 间距 Token（spacing scale）
- 圆角 Token（border-radius）
- 阴影 Token（box-shadow）
- 断点 Token（breakpoints）

**输出格式 — 现有 Token 摘要：**

```
| Token 类别 | Token 名称 | 当前值 | 来源文件 |
|---|---|---|---|
| 颜色 | --color-primary | #3B82F6 | tailwind.config.ts |
| 字体 | --font-size-base | 16px | theme.ts |
| 间距 | --spacing-4 | 16px | tailwind.config.ts |
| 圆角 | --radius-lg | 8px | tailwind.config.ts |
| 阴影 | --shadow-md | 0 4px 6px -1px rgba(0,0,0,0.1) | theme.ts |
```

**步骤 1.5: 读取路由配置 → 了解页面结构**

根据元框架类型读取路由配置：
- **Next.js App Router**: 扫描 `src/app/**/page.tsx`
- **Next.js Pages Router**: 读取 `src/pages/_app.tsx` 和目录结构
- **Vue Router**: 读取 `src/router/index.ts`
- **React Router**: 读取 `src/App.tsx` 或路由配置文件

**输出格式 — 路由结构表：**

```
| 路由路径 | 页面文件 | 页面组件 | 说明 |
|---|---|---|---|
| / | src/app/page.tsx | HomePage | 首页 |
| /dashboard | src/app/dashboard/page.tsx | DashboardPage | 仪表盘 |
| /settings | src/app/settings/page.tsx | SettingsPage | 设置页 |
```

---

### Phase 2: 设计数据采集

> **在 Phase 1 代码库分析的基础上，采集 Figma 设计数据，为后续对比做准备。**

**步骤 2.1: 验证连接状态**
- 使用 `get_document_info` 验证与 Figma 的连接是否正常
- 如果返回错误，回到 Phase 0 排查连接问题

**步骤 2.2: 采集基础设计数据**
按以下顺序调用 TalkToFigma 工具：

1. `get_document_info` → 获取文档基本信息（名称、页面结构）
2. `get_selection` → 获取当前选中节点的概要信息
3. `read_my_design` → 获取选中区域的完整设计数据（最详细）
4. `get_styles` → 获取文档中的所有样式定义
5. `get_local_components` → 获取本地组件列表（用于组件复用判断）
6. `export_node_as_image` → 导出选中节点的截图（用于后续视觉对比）

**如果选区过大或数据截断：**
- 使用 `scan_nodes_by_types` 按类型分批扫描
- 使用 `scan_text_nodes` 单独提取文本节点
- 使用 `get_node_info` / `get_nodes_info` 按需获取单个节点详情

**步骤 2.7: 资产清单采集**

使用 `scan_nodes_by_types` 筛选 `IMAGE` 和 `RECTANGLE` 类型的节点，列出所有需要导出的视觉资产。

**采集方法：**
1. `scan_nodes_by_types(types: ["IMAGE", "RECTANGLE"])` → 获取所有图片和纯色块节点
2. 对每个 IMAGE 节点，使用 `get_node_info` 获取：
   - 节点名称（用于命名文件）
   - 尺寸（width × height）
   - 类型（SVG/PNG/内联图标）
   - 填充模式（FILL/STROKE）
3. 过滤掉纯装饰性节点（如背景色块），保留功能性资产

**输出格式 — 资产清单表格：**

```
| # | 资产名称 | 类型 | 尺寸 | 导出格式 | 目标路径 | 备注 |
|---|---|---|---|---|---|---|
| 1 | logo-main | IMAGE | 120×32 | SVG | src/assets/icons/logo.svg | 品牌Logo |
| 2 | avatar-placeholder | IMAGE | 40×40 | PNG | src/assets/images/avatar.png | 头像占位 |
| 3 | icon-search | IMAGE | 20×20 | SVG | src/assets/icons/search.svg | 搜索图标 |
| 4 | bg-gradient-hero | RECTANGLE | 1920×600 | CSS | - | CSS渐变实现 |
| ~ | ... | ... | ... | ... | ... | ... |
```

**步骤 2.8: 精确布局尺寸采集**

使用 `get_node_info` 获取关键容器的精确尺寸信息，所有值精确到 px。

**采集目标：**
1. 页面整体容器（Frame）→ width / height
2. 侧边栏 → width / padding
3. 头部导航 → height / padding
4. 内容区域 → width / padding / gap
5. 卡片组件 → width / height / padding / border-radius
6. 网格布局 → columns / gap / column-width

**输出格式 — 精确布局尺寸表：**

```
| 容器/组件 | 宽度 | 高度 | 内边距 | 间距 | 圆角 | 备注 |
|---|---|---|---|---|---|---|
| 页面整体 | 1440px | 900px | - | - | - | 设计稿画布尺寸 |
| Header | 1440px | ~80px | 0 32px | - | - | 固定顶部 |
| Sidebar | ~350px | 100% | 24px | 8px | - | 左侧固定 |
| Main Content | ~430px | 100% | 24px | 16px | - | 右侧内容区 |
| Card | 100% | auto | 16px | - | 12px | 内容卡片 |
| Grid Gap | - | - | - | 16px | - | 卡片间距 |
```

---

### Phase 3: Figma 解释引擎处理

> **这是本技能的核心差异化能力。** 详见 `references/figma-interpreter-engine.md`

对采集到的原始设计数据执行以下处理：

1. **噪音过滤** — 移除不可见图层、重叠节点、空白元素
2. **结构修正** — 修正错误分组，还原设计师真实意图
3. **布局推断** — 理解 Auto Layout 语义，推断 Flex/Grid 布局
4. **组件识别** — 识别重复 UI 模式，标记为可复用组件
5. **层级规范化** — 统一节点层级，消除冗余嵌套

---

### Phase 4: 设计 Token 提取与验证

> **核心策略："Validate, Don't Rebuild" — 已有的 Token 只验证不重建。**
> **详见 `references/design-token-extraction.md`**

**步骤 4.1: Token 提取**

从清洗后的设计数据中精确提取以下 Token，精度要求精确到 px：

- 颜色（fill/stroke/text color，含透明度）
- 字体（font-family/font-size/font-weight/line-height/letter-spacing）
- 间距（padding/margin/gap）
- 圆角（border-radius）
- 阴影（box-shadow，含 offset/blur/spread/color）
- 边框（border-width/border-color/border-style）
- 尺寸（width/height/min-width/max-width）
- 透明度（opacity）

**步骤 4.2: Token 复用验证**

将 Figma 提取的 Token 与 Phase 1.4 中获取的现有项目 Token 进行逐一对比。

**对比规则：**

| 对比结果 | 标记 | 处理策略 |
|---|---|---|
| 值完全一致 | ✅ Match | 直接复用现有 Token，不创建新的 |
| 值接近（偏差 ≤ 1px） | ⚠️ Close | 使用现有 Token，记录偏差供审查 |
| 值差异明显 | ❌ Mismatch | 创建新 Token 或更新现有 Token |
| Figma 有但项目缺失 | ➕ New | 创建新 Token |
| 项目有但 Figma 未使用 | ➖ Unused | 标记为未使用，不删除 |

**输出格式 — Token 验证表格：**

```
| Token 类别 | Figma 值 | 项目现有值 | 状态 | 处理策略 |
|---|---|---|---|---|
| 颜色-Primary | #3B82F6 | #3B82F6 | ✅ Match | 复用 |
| 颜色-Background | #F8FAFC | #F9FAFB | ⚠️ Close | 复用，偏差 #010101 |
| 字体-Heading | Inter 24px Bold | Inter 24px Bold | ✅ Match | 复用 |
| 间距-Card Padding | 20px | 16px | ❌ Mismatch | 新建 Token |
| 颜色-Accent | #8B5CF6 | - | ➕ New | 创建新 Token |
```

---

### Phase 5: Gap Analysis

> **核心目的：明确现有代码与 Figma 设计之间的差距，决定每个组件的处理策略。**
> **详见 `references/gap-analysis.md`**

**分析对象：** Phase 1 代码库分析结果 vs Phase 2-4 设计数据采集结果

**步骤 5.1: 组件级 Gap Analysis**

对 Figma 设计中的每个 Section/组件，与现有代码进行逐一对比：

**输出格式 — Gap Analysis 表格：**

```
| # | Section/组件 | Figma 设计 | 现有代码 | 状态 | 关键差距 | 处理策略 |
|---|---|---|---|---|---|---|
| 1 | Header 导航栏 | 固定顶部, 高80px, 深色背景 | Header.tsx 存在 | ⚠️ Audit Needed | 高度不匹配, 缺少搜索框 | 修改现有组件 |
| 2 | Sidebar 侧边栏 | 宽350px, 可折叠, 菜单树 | Sidebar.tsx 存在 | ⚠️ Audit Needed | 缺少折叠功能, 图标不匹配 | 修改现有组件 |
| 3 | Dashboard 卡片网格 | 3列, gap 16px, 圆角12px | 无对应组件 | ❌ Missing | 完全缺失 | 新建组件 |
| 4 | 数据表格 | 斑马纹, 排序, 分页 | DataTable.tsx 存在 | ✅ Complete | 样式基本一致 | 仅验证 |
| 5 | 用户头像下拉菜单 | 头像+下拉+角色标签 | 无对应组件 | ❌ Missing | 完全缺失 | 新建组件 |
| 6 | 底部状态栏 | 固定底部, 状态指示器 | Footer.tsx 存在 | ⚠️ Audit Needed | 样式差异大 | 重构现有组件 |
```

**步骤 5.2: 资产级 Gap Analysis**

对比资产清单（Phase 2.7）与现有静态资源：

```
| 资产名称 | Figma 需要 | 项目现有 | 状态 | 处理方式 |
|---|---|---|---|---|
| logo.svg | ✅ | ✅ src/assets/logo.svg | ✅ Match | 复用 |
| search-icon.svg | ✅ | ❌ | ❌ Missing | 从 Figma 导出 |
| avatar-default.png | ✅ | ✅ src/assets/avatar.png | ⚠️ Different | 替换为新版本 |
```

**步骤 5.3: Token 级 Gap Analysis**

汇总 Phase 4.2 的 Token 验证结果，按影响范围排序：

```
| 影响范围 | Token 差异数 | 新建数 | 修改数 | 复用数 |
|---|---|---|---|---|
| 颜色 | 5 | 2 | 1 | 2 |
| 字体 | 3 | 1 | 0 | 2 |
| 间距 | 4 | 2 | 1 | 1 |
| 圆角 | 2 | 1 | 0 | 1 |
| 阴影 | 1 | 1 | 0 | 0 |
| **合计** | **15** | **7** | **2** | **6** |
```

**步骤 5.4: 汇总差距报告**

根据以上分析，输出差距汇总：

```
## Gap Analysis 汇总

### 统计概览
- ✅ Complete（可直接复用）: X 个
- ⚠️ Audit Needed（需要修改）: X 个
- ❌ Missing（需要新建）: X 个

### 工作量估算
- 新建组件: X 个
- 修改组件: X 个
- 仅验证组件: X 个
- 新建 Token: X 个
- 导出资产: X 个
```

---

### Phase 6: 代码生成

> **根据 Gap Analysis 结果决定生成策略，避免重复造轮子。**
> **详见 `references/code-generation-rules.md`**

**步骤 6.1: 确定生成策略**

根据 Phase 5 的 Gap Analysis 结果，对每个组件采用不同策略：

| Gap 状态 | 生成策略 | 说明 |
|---|---|---|
| ✅ Complete | **验证模式** | 不修改代码，仅验证现有实现与设计的一致性 |
| ⚠️ Audit Needed | **修改模式** | 在现有组件基础上修改样式/结构/功能 |
| ❌ Missing | **新建模式** | 从零创建新组件 |

**步骤 6.2: 资产导出与引用**

根据 Phase 2.7 的资产清单，批量导出所需资产：

1. 对标记为 ❌ Missing 的资产，使用 `export_node_as_image` 导出
2. 将导出的资产保存到项目对应的目录（如 `src/assets/icons/`、`src/assets/images/`）
3. 在生成的代码中使用正确的相对路径引用资产

**步骤 6.3: 代码生成规则**

**目标技术栈：** 使用 Phase 1.1 检测到的技术栈，不擅自更换。

**核心规则：**
1. **优先复用** — ✅ Complete 的组件直接引用，不重新生成
2. **Token 优先** — 使用 Phase 4 验证通过的 Token，不硬编码颜色/间距
3. **组件对齐** — 组件粒度与 Figma 组件对齐，每个设计节点对应一个组件
4. **布局转换** — 将 Figma 的 Auto Layout 转换为 Flexbox/Grid
5. **精确尺寸** — 使用 Phase 2.8 采集的精确 px 值
6. **真实文本** — 使用 Figma 中的真实文本，不使用 Lorem ipsum
7. **遵循约定** — 遵循项目的文件结构、命名约定和代码风格

**步骤 6.4: 按优先级生成**

按以下优先级顺序生成代码：
1. **基础组件**（Button/Input/Modal 等）→ 被其他组件依赖
2. **布局组件**（Header/Sidebar/Layout 等）→ 页面骨架
3. **业务组件**（Dashboard Card/Table 等）→ 页面内容
4. **页面组装**（将组件组合为完整页面）

---

### Phase 7: 交互状态规划

> **从 Figma 设计中识别所有交互状态，确保还原不仅是静态的，还包括动态行为。**

**步骤 7.1: 识别交互状态**

从 Figma 设计数据中识别以下状态：

| 状态类型 | 说明 | 检测方法 |
|---|---|---|
| hover | 鼠标悬停 | 查找 `[hover]` 命名的变体或组件属性 |
| active/pressed | 按下状态 | 查找 `[active]` / `[pressed]` 变体 |
| focus | 焦点状态 | 查找 `[focus]` / `[focused]` 变体 |
| disabled | 禁用状态 | 查找 `[disabled]` 变体 |
| selected | 选中状态 | 查找 `[selected]` 变体 |
| error | 错误状态 | 查找 `[error]` 变体 |
| loading | 加载状态 | 查找 `[loading]` 变体 |
| expanded/collapsed | 展开/折叠 | 查找 `[open]` / `[closed]` 变体 |

**步骤 7.2: 规划过渡动画**

为状态切换规划过渡效果：

```
| 组件 | 触发状态 | 过渡属性 | 持续时间 | 缓动函数 |
|---|---|---|---|---|
| Button | hover → default | background-color, box-shadow | 150ms | ease-in-out |
| Button | active → default | transform (scale 0.98) | 100ms | ease-out |
| Sidebar | expanded → collapsed | width, opacity | 300ms | cubic-bezier(0.4, 0, 0.2, 1) |
| Card | hover → default | box-shadow, transform (translateY -2px) | 200ms | ease-in-out |
| Modal | open → closed | opacity, transform (scale) | 200ms | ease-out |
| Input | focus → default | border-color, box-shadow | 150ms | ease-in-out |
| Dropdown | open → closed | opacity, transform (translateY) | 150ms | ease-out |
```

**步骤 7.3: 规划滚动行为**

```
| 容器 | 滚动方向 | 溢出处理 | 滚动条样式 | 备注 |
|---|---|---|---|---|
| Main Content | 纵向 | overflow-y: auto | 自定义细滚动条 | 主内容区 |
| Sidebar Menu | 纵向 | overflow-y: auto | 自定义细滚动条 | 菜单项过多时 |
| Table Body | 纵向 | overflow-y: auto | 自定义细滚动条 | 固定表头 |
| Horizontal Scroll | 横向 | overflow-x: auto | 隐藏滚动条 | 卡片横向滚动 |
```

**步骤 7.4: 输出交互状态清单**

将以上信息汇总为完整的交互状态清单，供代码生成阶段使用。

---

### Phase 8: 浏览器验证引擎

> **详见 `references/browser-verification-engine.md`**

**步骤 8.1: 渲染验证**
1. 启动本地开发服务器（如 `npm run dev`）
2. 使用 `browser_navigate` 打开生成的页面
3. 使用 `browser_take_screenshot` 截取渲染结果

**步骤 8.2: DOM/CSS 精确对比**
1. 使用 `browser_snapshot` 获取 DOM 结构
2. 使用 `browser_evaluate` 提取关键元素的 CSS 计算值
3. 将提取的 CSS 值与设计 Token 逐一对比

**步骤 8.3: 像素级视觉对比**
1. 将 Figma 导出的截图与浏览器截图进行视觉对比
2. 识别差异区域（颜色偏差、间距偏差、尺寸偏差、对齐偏差）
3. 生成差异报告

**步骤 8.4: 自动修复**
1. 根据差异报告，定位需要修改的代码位置
2. 调整 CSS 属性值（如间距、颜色、字体大小）
3. 重新渲染并验证，直到差异在可接受范围内

---

### Phase 9: 交付与验收

**步骤 9.1: Definition of Done 清单**

```
## Definition of Done

### 功能完整性
- [ ] 所有 Figma 设计中的 Section/组件已实现
- [ ] 所有交互状态（hover/active/focus/disabled）已实现
- [ ] 所有过渡动画已实现
- [ ] 所有资产（SVG/PNG）已正确导出和引用

### 视觉保真度
- [ ] 颜色还原：ΔE < 2（人眼不可感知）
- [ ] 间距还原：偏差 ≤ 1px
- [ ] 字体还原：字号偏差 ≤ 1px，字重完全一致
- [ ] 布局还原：元素位置偏差 ≤ 2px
- [ ] 圆角还原：偏差 ≤ 1px
- [ ] 阴影还原：视觉一致

### 代码质量
- [ ] 代码结构清晰、可维护
- [ ] 遵循项目现有代码规范
- [ ] Token 复用率 ≥ 60%（已有 Token 优先复用）
- [ ] 组件复用率 ≥ 40%（已有组件优先复用）
- [ ] 无硬编码的颜色/间距值

### 响应式
- [ ] 目标视口（如 1920×1080）渲染正确
- [ ] 断点切换正常（如需要）
```

**步骤 9.2: 目标视口标注**

明确设计稿的目标视口，在交付时标注：

```
| 属性 | 值 |
|---|---|
| 设计稿尺寸 | 1440 × 900 px |
| 目标视口 | 1920 × 1080 px（全屏） |
| 设备类型 | Desktop |
| 缩放比例 | 100% |
| 浏览器 | Chrome 最新版 |
```

**步骤 9.3: 最终交付**
1. 确认所有组件渲染正确
2. 确认响应式布局正常
3. 确认代码结构清晰、可维护
4. 输出最终代码文件
5. 输出 Gap Analysis 对比报告（Phase 5 的最终版）
6. 输出 Token 验证报告（Phase 4.2 的最终版）

---

## Plan 生成模式

> **当用户要求生成 Plan（而非直接执行代码生成）时，按以下步骤引导输出完整的实施计划。**
> **触发方式：`为 Figma 设计稿 [URL] 生成像素级还原 Plan`**

### Plan 生成步骤

**Step 1: 技术栈识别**

读取 `package.json`，输出 Tech Stack Preferences 表格：

```
## 1. Tech Stack Preferences

| 类别 | 当前技术 | 版本 | 备注 |
|---|---|---|---|
| 框架 | React | 18.2.0 | - |
| 元框架 | Next.js | 14.1.0 | App Router |
| 样式方案 | Tailwind CSS | 3.4.1 | - |
| 组件库 | 自定义 | - | src/components/ui/ |
| TypeScript | 是 | 5.3.0 | strict mode |
| 图标库 | Lucide React | 0.344.0 | - |
| 状态管理 | Zustand | 4.5.0 | - |
```

**Step 2: 组件架构梳理**

扫描 `src/` 目录，输出组件树：

```
## 2. Component Architecture

```
src/
├── app/                          # Next.js App Router
│   ├── layout.tsx                # 根布局
│   ├── page.tsx                  # 首页
│   └── dashboard/
│       └── page.tsx              # 仪表盘页
├── components/
│   ├── ui/                       # 基础 UI 组件（8 个）
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   ├── Card.tsx
│   │   ├── Badge.tsx
│   │   ├── Avatar.tsx
│   │   ├── Dropdown.tsx
│   │   └── Tooltip.tsx
│   ├── layout/                   # 布局组件（3 个）
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   └── features/                 # 业务组件
│       ├── Dashboard/
│       └── Settings/
├── lib/                          # 工具库
│   └── utils.ts
├── hooks/                        # 自定义 Hooks
├── store/                        # 状态管理
└── types/                        # 类型定义
```
```

**Step 3: Gap Analysis**

对比现有代码 vs Figma 设计，输出状态表格：

```
## 3. Gap Analysis

| # | 组件/Section | Figma 设计 | 现有代码 | 状态 | 关键差距 |
|---|---|---|---|---|---|
| 1 | Header | 固定顶部, 80px高 | Header.tsx | ⚠️ | 高度不匹配, 缺搜索框 |
| 2 | Sidebar | 350px宽, 可折叠 | Sidebar.tsx | ⚠️ | 缺折叠, 图标不匹配 |
| 3 | Stats Cards | 4列卡片网格 | 无 | ❌ | 完全缺失 |
| 4 | Data Table | 排序+分页 | DataTable.tsx | ✅ | 样式一致 |
| 5 | Activity Feed | 时间线列表 | 无 | ❌ | 完全缺失 |
| 6 | User Menu | 头像下拉 | 无 | ❌ | 完全缺失 |

### 统计
- ✅ 可复用: 1 个
- ⚠️ 需修改: 2 个
- ❌ 需新建: 3 个
```

**Step 4: 布局策略**

从 Figma 数据提取精确尺寸，输出 ASCII 布局图：

```
## 4. Layout Strategy

### 目标视口: 1440 × 900 px

```
┌─────────────────────────────────────────────────────────┐
│  Header (h: 80px, px: 0 32px)                          │
│  [Logo] [Nav Items...]              [Search] [Avatar▼]  │
├──────────────┬──────────────────────────────────────────┤
│              │                                           │
│  Sidebar     │  Main Content (px: 24px, gap: 16px)      │
│  (w: 350px)  │                                           │
│  (px: 24px)  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│              │  │Card 1│ │Card 2│ │Card 3│ │Card 4│   │
│  [Menu 1]    │  │h:120 │ │h:120 │ │h:120 │ │h:120 │   │
│  [Menu 2]    │  └──────┘ └──────┘ └──────┘ └──────┘   │
│  [Menu 3]    │                                           │
│  [Menu 4]    │  ┌────────────────────────────────────┐  │
│              │  │         Data Table                  │  │
│              │  │         (h: ~400px)                 │  │
│              │  └────────────────────────────────────┘  │
│              │                                           │
├──────────────┴──────────────────────────────────────────┤
│  Footer (h: 48px)                                       │
└─────────────────────────────────────────────────────────┘

总宽度: 1440px
Sidebar: 350px | Main: 1440 - 350 = 1090px
Grid: 4 列, gap: 16px, 列宽: (1090 - 48 - 48) / 4 ≈ 248px
```
```

**Step 5: 状态管理分析**

读取现有状态管理模式：

```
## 5. State Management

| 状态类型 | 管理方式 | 文件位置 | 备注 |
|---|---|---|---|
| 全局状态 | Zustand | src/store/ | 用户信息、主题设置 |
| 服务端状态 | React Query | src/hooks/ | 数据获取、缓存 |
| 组件状态 | useState | 各组件内 | 表单、弹窗开关 |
| URL 状态 | Next.js Router | - | 页面路由、查询参数 |
```

**Step 6: 分阶段路线图**

输出 Phased Development Roadmap：

```
## 6. Phased Development Roadmap

| Phase | 内容 | 组件数 | 预估工作量 | 依赖 |
|---|---|---|---|---|
| Phase 0 | 环境准备 + Token 验证 | - | 0.5h | - |
| Phase 1 | 基础组件验证/修改 | 2 | 1h | Phase 0 |
| Phase 2 | 布局组件修改 | 2 | 1.5h | Phase 1 |
| Phase 3 | 业务组件新建 | 3 | 3h | Phase 2 |
| Phase 4 | 资产导出 + 引用 | ~10 | 0.5h | Phase 0 |
| Phase 5 | 交互状态 + 动画 | - | 1h | Phase 3 |
| Phase 6 | 页面组装 + 集成 | 1 | 1h | Phase 3-5 |
| Phase 7 | 浏览器验证 + 修复 | - | 1h | Phase 6 |
| **合计** | | **8** | **~9h** | |
```

**Step 7: 像素级保真策略**

```
## 7. Fidelity Strategy

| 维度 | 保真目标 | 验证方法 | 容差 |
|---|---|---|---|
| 颜色 | 完全匹配 | CSS 值对比 | ΔE < 2 |
| 字体 | 完全匹配 | CSS 值对比 | ≤ 1px |
| 间距 | 完全匹配 | CSS 值对比 | ≤ 1px |
| 圆角 | 完全匹配 | CSS 值对比 | ≤ 1px |
| 阴影 | 视觉一致 | 视觉对比 | - |
| 布局 | 完全匹配 | 视觉对比 | ≤ 2px |
| 图标 | 完全匹配 | 视觉对比 | - |
| 动画 | 流畅自然 | 手动测试 | - |
```

**Step 8: Definition of Done**

```
## 8. Definition of Done

- [ ] 所有 Figma Section 已实现（✅/⚠️/❌ 全部处理）
- [ ] 所有交互状态已实现（hover/active/focus/disabled）
- [ ] 所有过渡动画已实现（duration + easing 正确）
- [ ] 所有资产已导出并正确引用
- [ ] Token 复用率 ≥ 60%
- [ ] 组件复用率 ≥ 40%
- [ ] 目标视口（1920×1080）渲染正确
- [ ] 浏览器验证通过（颜色/间距/字体/布局偏差在容差内）
- [ ] 代码遵循项目规范
```

**Step 9: TODO 列表**

```
## 9. TODOs

### Phase 0: 环境准备
- [ ] [Phase 0] 验证 Figma 连接，确认选区
- [ ] [Phase 0] 读取 package.json，确认技术栈
- [ ] [Phase 0] 扫描目录结构，识别组件体系
- [ ] [Phase 0] 读取现有 Token 文件
- [ ] [Phase 0] 执行 Token 复用验证

### Phase 1: 基础组件
- [ ] [Phase 1] 验证 Button.tsx 样式一致性
- [ ] [Phase 1] 修改 Card.tsx 圆角为 12px
- [ ] [Phase 1] 新建 Badge.tsx 组件

### Phase 2: 布局组件
- [ ] [Phase 2] 修改 Header.tsx 高度为 80px，添加搜索框
- [ ] [Phase 2] 修改 Sidebar.tsx 宽度为 350px，添加折叠功能

### Phase 3: 业务组件
- [ ] [Phase 3] 新建 StatsCard.tsx（4列网格布局）
- [ ] [Phase 3] 新建 ActivityFeed.tsx（时间线列表）
- [ ] [Phase 3] 新建 UserMenu.tsx（头像下拉菜单）

### Phase 4: 资产
- [ ] [Phase 4] 导出 logo.svg → src/assets/icons/logo.svg
- [ ] [Phase 4] 导出 search-icon.svg → src/assets/icons/search.svg
- [ ] [Phase 4] 导出 avatar-default.png → src/assets/images/avatar.png

### Phase 5: 交互状态
- [ ] [Phase 5] 实现 Button hover/active 状态
- [ ] [Phase 5] 实现 Card hover 阴影效果
- [ ] [Phase 5] 实现 Sidebar 折叠动画（300ms ease）
- [ ] [Phase 5] 实现 Input focus 边框效果

### Phase 6: 页面组装
- [ ] [Phase 6] 组装 Dashboard 页面布局
- [ ] [Phase 6] 集成所有组件到页面

### Phase 7: 验证
- [ ] [Phase 7] 启动 dev server，浏览器验证
- [ ] [Phase 7] 像素级对比，生成差异报告
- [ ] [Phase 7] 修复所有超出容差的差异
```

---

## Prompt 模式

### 基础模式 — 直接代码生成
```
将 Figma 选区转换为 React + Tailwind 代码
```

### Plan 生成模式 — 生成实施计划
```
为 Figma 设计稿 [URL] 生成像素级还原 Plan
```

### Gap 分析模式 — 仅分析差距
```
分析现有代码与 Figma 设计的差距
```

### Token 验证模式 — 仅验证 Token
```
验证现有 Token 与 Figma 设计的一致性
```

### 指定技术栈
```
将 Figma 选区转换为 Vue 3 + CSS Modules 代码
```

### 使用项目组件
```
将 Figma 选区转换为代码，使用 src/components/ui 中的组件
```

### 仅提取设计 Token
```
从 Figma 选区中提取所有设计 Token（颜色、字体、间距等）
```

### 仅验证模式
```
验证当前页面与 Figma 设计稿的像素级一致性
```

---

## References

- `references/figma-interpreter-engine.md` — Figma 解释引擎详细规范
- `references/design-token-extraction.md` — 设计 Token 提取规范
- `references/browser-verification-engine.md` — 浏览器验证引擎详细规范
- `references/code-generation-rules.md` — 代码生成规则和最佳实践
- `references/codebase-analysis.md` — 代码库分析方法论
- `references/gap-analysis.md` — Gap Analysis 方法论

---

## 验证标准

| 检查项 | 标准 | 验证方式 |
|---|---|---|
| 颜色还原 | ΔE < 2（人眼不可感知） | CSS 值对比 |
| 间距还原 | 偏差 ≤ 1px | CSS 值对比 |
| 字体还原 | 字号偏差 ≤ 1px，字重完全一致 | CSS 值对比 |
| 布局还原 | 元素位置偏差 ≤ 2px | 视觉对比 |
| 圆角还原 | 偏差 ≤ 1px | CSS 值对比 |
| 阴影还原 | 视觉一致 | 视觉对比 |
| 组件结构 | 与 Figma 组件一一对应 | DOM 结构对比 |
| Token 复用率 | ≥ 60%（已有 Token 优先复用） | Token 对比报告 |
| 组件复用率 | ≥ 40%（已有组件优先复用） | Gap Analysis 报告 |
| 交互状态 | hover/active/focus 状态完整 | 手动测试 + 代码审查 |
| 过渡动画 | duration 和 easing 与设计一致 | 手动测试 |
