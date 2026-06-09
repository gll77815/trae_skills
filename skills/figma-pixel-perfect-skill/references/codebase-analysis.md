# 代码库分析方法论

> 本文档是 `figma-pixel-perfect` 技能 Phase 1 的详细参考。
> 在生成代码之前，必须先彻底理解现有项目的结构、技术栈、组件体系和 Token 系统。

## 核心原则

**"先理解，再动手"** — 代码库分析是像素级还原的基石。跳过此阶段会导致：
- 生成与项目风格不一致的代码
- 重复创建已有的组件和 Token
- 破坏项目现有的架构约定

## 分析步骤详解

### 步骤 1.1: 读取 package.json

**目的：** 快速了解项目的技术栈全貌。

**操作方法：**
1. 使用 Read 工具读取项目根目录的 `package.json`
2. 解析 `dependencies` 和 `devDependencies` 字段
3. 提取关键信息

**关键识别规则：**

| 依赖包名 | 识别为 | 说明 |
|---|---|---|
| `react` | React 框架 | 检查版本号 |
| `vue` | Vue 框架 | 检查版本号（Vue 2/3） |
| `next` | Next.js 元框架 | 检查版本号，判断 App Router / Pages Router |
| `nuxt` | Nuxt 元框架 | 检查版本号 |
| `tailwindcss` | Tailwind CSS | 检查版本号 |
| `styled-components` | Styled Components | CSS-in-JS 方案 |
| `@mui/material` | MUI 组件库 | Material Design 组件 |
| `antd` | Ant Design | Ant Design 组件 |
| `@heroicons/react` | Heroicons 图标库 | - |
| `lucide-react` | Lucide 图标库 | - |
| `typescript` | TypeScript | 检查版本号和 strict 配置 |
| `zustand` | Zustand 状态管理 | - |
| `@tanstack/react-query` | React Query | 服务端状态管理 |

**输出要求：**
- 必须输出技术栈表格（见 SKILL.md Phase 1.1）
- 如果检测到不熟悉的技术栈，应在表格中标注并提醒用户确认

### 步骤 1.2: 扫描目录结构

**目的：** 了解项目的文件组织方式，确定代码生成时的文件放置位置。

**操作方法：**
1. 使用 Glob 工具扫描根目录：`*`
2. 使用 Glob 工具扫描 src 目录：`src/*` 和 `src/**/*`
3. 识别关键目录模式

**目录识别规则：**

| 目录模式 | 含义 | 代码生成时的用途 |
|---|---|---|
| `src/components/**` | 组件目录 | 新建组件放在这里 |
| `src/components/ui/**` | 基础 UI 组件 | 优先复用这些组件 |
| `src/components/layout/**` | 布局组件 | 布局组件放在这里 |
| `src/pages/**` | 页面目录（Pages Router） | 页面文件放在这里 |
| `src/app/**` | 页面目录（App Router） | 页面文件放在这里 |
| `src/styles/**` | 样式目录 | 全局样式放在这里 |
| `src/assets/**` | 静态资源目录 | 导出的资产放在这里 |
| `src/types/**` | 类型定义目录 | 新增类型放在这里 |
| `src/hooks/**` | 自定义 Hooks | 新增 Hooks 放在这里 |
| `src/store/**` | 状态管理目录 | 状态相关代码放在这里 |
| `public/**` | 公共静态资源 | 不需要编译的资源放在这里 |

**特殊情况处理：**
- 如果没有 `src/` 目录，组件可能在根目录的 `components/` 下
- 如果没有 `components/` 目录，需要询问用户组件应放在哪里
- 如果有 `packages/` 目录，可能是 monorepo，需要进一步确认目标包

### 步骤 1.3: 读取现有组件

**目的：** 列出所有已有组件，避免重复创建。

**操作方法：**
1. 使用 Glob 扫描组件目录：`src/components/**/*.{tsx,jsx,vue,ts,js}`
2. 对每个组件文件，读取文件内容
3. 提取组件名称、Props 接口、职责描述

**组件信息提取规则：**

```
对于 React 组件：
- 组件名 = 文件名（PascalCase）或 export default 的名称
- Props = interface/type 定义中的属性列表
- 职责 = 从文件名 + 代码注释 + JSX 结构推断

对于 Vue 组件：
- 组件名 = defineComponent 的 name 或文件名
- Props = defineProps 中的属性列表
- 职责 = 从文件名 + template 结构推断
```

**输出要求：**
- 必须输出组件架构树（见 SKILL.md Phase 1.3）
- 对于每个组件，至少包含：文件路径、组件名、职责描述
- 如果组件数量超过 20 个，只列出与 Figma 设计相关的组件

### 步骤 1.4: 读取现有 Token

**目的：** 了解项目已有的设计系统，为 Token 复用验证做准备。

**操作方法：**
1. 按优先级搜索 Token 文件
2. 读取找到的 Token 文件
3. 提取所有 Token 值

**搜索优先级：**

| 优先级 | 文件模式 | 说明 |
|---|---|---|
| 1 | `**/figmaDesignTokens.ts` | 专门的 Figma Token 文件（最高优先级） |
| 2 | `**/theme.ts` | 主题配置文件 |
| 3 | `**/tokens.ts` | Token 定义文件 |
| 4 | `tailwind.config.{ts,js}` | Tailwind 配置中的 theme 扩展 |
| 5 | `**/*.css` 中的 `:root` | CSS 变量定义 |

**Token 分类提取：**

| Token 类别 | 提取内容 | 示例 |
|---|---|---|
| 颜色 | primary/secondary/success/warning/error/neutral | `#3B82F6` |
| 字体 | font-family/font-size/font-weight/line-height | `Inter 16px 400 1.5` |
| 间距 | spacing scale（4/8/12/16/20/24...） | `16px` |
| 圆角 | border-radius（sm/md/lg/full） | `8px` |
| 阴影 | box-shadow（sm/md/lg/xl） | `0 4px 6px -1px rgba(0,0,0,0.1)` |
| 断点 | breakpoints（sm/md/lg/xl/2xl） | `768px` |
| 动画 | transition duration/easing | `150ms ease-in-out` |

**输出要求：**
- 必须输出现有 Token 摘要表格（见 SKILL.md Phase 1.4）
- 包含 Token 名称、当前值、来源文件路径
- 如果未找到任何 Token 文件，标注为"项目无现有 Token 系统"

### 步骤 1.5: 读取路由配置

**目的：** 了解项目的页面结构，确定代码生成时的目标页面。

**操作方法：**

根据检测到的元框架类型，采用不同的读取策略：

**Next.js App Router：**
```
扫描 src/app/**/page.tsx
扫描 src/app/**/layout.tsx
```

**Next.js Pages Router：**
```
读取 src/pages/_app.tsx
扫描 src/pages/**/*.tsx
```

**Vue Router：**
```
读取 src/router/index.ts
```

**React Router：**
```
读取 src/App.tsx（查找 <Route> 组件）
或读取 src/routes.tsx
```

**输出要求：**
- 必须输出路由结构表（见 SKILL.md Phase 1.5）
- 包含路由路径、页面文件、页面组件名、说明

## 分析结果汇总

完成所有步骤后，输出以下汇总信息：

```
## 代码库分析汇总

### 技术栈
- 框架: React 18.2.0
- 元框架: Next.js 14.1.0 (App Router)
- 样式: Tailwind CSS 3.4.1
- TypeScript: 5.3.0 (strict)

### 组件体系
- 基础 UI 组件: 8 个（Button, Input, Modal, Card, Badge, Avatar, Dropdown, Tooltip）
- 布局组件: 3 个（Header, Sidebar, Footer）
- 业务组件: 2 个（Dashboard, Settings）

### Token 系统
- Token 文件: tailwind.config.ts, src/styles/globals.css
- 颜色 Token: 12 个
- 字体 Token: 6 个
- 间距 Token: 8 个

### 路由结构
- 页面数: 5 个
- 主要页面: /, /dashboard, /settings, /profile, /login

### 代码生成建议
- 新组件放置: src/components/features/
- 新 Token 添加: tailwind.config.ts theme.extend
- 资产放置: src/assets/icons/, src/assets/images/
```

## 常见问题处理

### Q: 项目没有 package.json
- 可能是纯 HTML/CSS 项目，使用默认配置（HTML + CSS）
- 询问用户确认技术栈

### Q: 项目使用 Monorepo
- 询问用户目标包是哪个
- 分析目标包的 package.json 和目录结构

### Q: 找不到 Token 文件
- 标注为"项目无现有 Token 系统"
- 在代码生成阶段创建新的 Token 系统

### Q: 组件使用非标准命名
- 按实际命名输出，不做重命名
- 在代码生成时遵循项目现有命名约定
