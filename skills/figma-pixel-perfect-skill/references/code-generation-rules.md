# 代码生成规则

## 概述

本规范定义了如何将 Figma 解释引擎处理后的设计语义数据转换为高质量的前端代码。核心原则：**生成的代码应该像人类开发者写的，而不是 AI 生成的。**

本规范为**技术栈无关**的设计，支持 Tailwind CSS、Less、Sass、CSS Modules、Inline Styles 等各种样式方案。生成代码时必须**尊重项目现有的样式方案和技术栈**，而非强加某一特定方案。

## 技术栈检测

在生成代码之前，必须先检测用户项目的技术栈：

```
检测优先级：
1. 检查 package.json → 确定框架（React/Vue/Next/Nuxt）
2. 检查 tailwind.config.js / tailwind.config.ts → 确定是否使用 Tailwind
3. 检查 src/components/ → 确定组件库（MUI/Ant Design/自定义）
4. 检查 tsconfig.json / jsconfig.json → 确定是否使用 TypeScript
5. 检查现有文件结构 → 确定命名约定和文件组织方式
```

### 样式方案检测

除了上述基础检测外，还需额外检测项目的样式方案：

```
样式方案检测项：
1. 检查 .less 文件 → 项目使用 Less 预处理器
2. 检查 .scss / .sass 文件 → 项目使用 Sass/SCSS 预处理器
3. 检查 .module.css / .module.less / .module.scss 文件 → 项目使用 CSS Modules
4. 检查 .css 文件（无 module 后缀）→ 项目使用原生 CSS
5. 检查 tailwind.config.js / tailwind.config.ts → 项目使用 Tailwind CSS
6. 检查 styled-components / emotion 等依赖 → 项目使用 CSS-in-JS
7. grep style={{ → 项目中存在 inline styles 使用习惯
```

### Token 系统检测

```
Token 文件检测项：
1. 检查 figmaDesignTokens.ts / figmaDesignTokens.js → Figma Token 映射文件
2. 检查 tokens.ts / tokens.js / tokens.json → 通用 Token 文件
3. 检查 theme.ts / theme.js → 主题配置文件
4. 检查 variables.less / variables.scss / variables.css → 样式变量文件
5. 检查 design-tokens.ts / designTokens.ts → 其他常见 Token 命名
```

### 全局样式检测

```
全局样式检测项：
1. 检查 index.less / index.scss / index.css → 全局入口样式
2. 检查 global.less / global.scss / global.css → 全局样式文件
3. 检查 styles/ / assets/styles/ 目录 → 样式文件目录
4. 检查 App.less / App.scss → 应用级样式
```

### 默认策略

**如果用户未指定技术栈，基于检测结果自动适配；如果无法检测，询问用户确认技术栈和样式方案。**

## 组件生成规则

### 1. 组件粒度

| Figma 节点类型 | 生成策略 |
|---|---|
| COMPONENT / COMPONENT_SET | 生成独立组件文件 |
| FRAME（有命名） | 生成独立组件文件 |
| FRAME（无命名/辅助） | 生成内联 div |
| GROUP | 不生成组件，展平为 div |
| TEXT | 生成语义化文本元素 |
| RECTANGLE（有填充） | 生成 div 或语义化元素 |
| IMAGE | 生成 img 元素 |
| INSTANCE | 复用已有组件，传入 Props |

### 2. 组件命名

```
Figma 名称 → 组件名称映射规则：
- "Header" → Header.tsx
- "Card / Default" → Card.tsx
- "Button / Primary" → ButtonPrimary.tsx
- "List Item" → ListItem.tsx
- "icon-search" → SearchIcon.tsx

命名规范：
- 使用 PascalCase
- 移除特殊字符（/、\、:）
- 移除状态后缀（/ Hover、/ Active、/ Disabled）
- 移除尺寸后缀（/ Desktop、/ Mobile）
```

### 3. 组件结构

```tsx
// 标准组件结构（样式方案根据项目检测结果选择）
import React from 'react';

// 1. 类型定义
interface HeaderProps {
  title: string;
  subtitle?: string;
  onMenuClick?: () => void;
}

// 2. 组件实现
export default function Header({ title, subtitle, onMenuClick }: HeaderProps) {
  return (
    <header className="header">
      <div className="header__content">
        <h1 className="header__title">{title}</h1>
        {subtitle && (
          <p className="header__subtitle">{subtitle}</p>
        )}
      </div>
      <button
        onClick={onMenuClick}
        className="header__menu-btn"
        aria-label="打开菜单"
      >
        <MenuIcon />
      </button>
    </header>
  );
}
```

### 4. 文件组织

```
src/
├── components/
│   ├── Header/
│   │   ├── Header.tsx          # 组件实现
│   │   ├── Header.module.css   # 样式（如使用 CSS Modules）
│   │   └── index.ts            # 导出
│   ├── Card/
│   │   ├── Card.tsx
│   │   └── index.ts
│   └── ui/                     # 通用 UI 组件
│       ├── Button.tsx
│       └── Input.tsx
├── pages/
│   └── HomePage.tsx            # 页面组件
├── styles/
│   └── tokens.css              # 设计 Token
└── types/
    └── index.ts                # 类型定义
```

## 布局转换规则

### Figma Auto Layout → CSS Flexbox 通用映射

| Figma 属性 | CSS 属性 |
|---|---|
| `layoutMode: HORIZONTAL` | `display: flex; flex-direction: row` |
| `layoutMode: VERTICAL` | `display: flex; flex-direction: column` |
| `primaryAxisAlignItems: MIN` | `justify-content: flex-start` |
| `primaryAxisAlignItems: CENTER` | `justify-content: center` |
| `primaryAxisAlignItems: MAX` | `justify-content: flex-end` |
| `primaryAxisAlignItems: SPACE_BETWEEN` | `justify-content: space-between` |
| `counterAxisAlignItems: MIN` | `align-items: flex-start` |
| `counterAxisAlignItems: CENTER` | `align-items: center` |
| `counterAxisAlignItems: MAX` | `align-items: flex-end` |
| `layoutSizing: HUG` | `width: fit-content` 或 `width: auto` |
| `layoutSizing: FILL` | `width: 100%` 或 `flex: 1` |
| `itemSpacing: N` | `gap: Npx` |
| `paddingTop/Right/Bottom/Left` | `padding: T R B L` |
| `layoutWrap: WRAP` | `flex-wrap: wrap` |

### Figma Auto Layout → Less 变量示例

```less
// 将 Figma Auto Layout 的间距、尺寸提取为 Less 变量
// 适用于项目使用 Less 预处理器的场景

@header-padding: 24px;          // Figma: paddingTop=24, paddingBottom=24
@header-padding-horizontal: 24px; // Figma: paddingLeft=24, paddingRight=24
@header-gap: 12px;              // Figma: itemSpacing=12
@content-max-width: 1200px;     // Figma: layoutSizing=FILL, maxWidth=1200

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: @header-padding @header-padding-horizontal;
  max-width: @content-max-width;
  gap: @header-gap;
}
```

### Figma Auto Layout → CSS Modules 示例

```css
/* Card.module.css — 将 Figma Auto Layout 转换为 CSS Modules */
/* 每个组件对应一个独立的 .module.css 文件，避免样式冲突 */

.container {
  display: flex;
  flex-direction: column;       /* Figma: layoutMode=VERTICAL */
  align-items: flex-start;      /* Figma: counterAxisAlignItems=MIN */
  gap: 16px;                    /* Figma: itemSpacing=16 */
  padding: 24px;                /* Figma: padding=24 */
  width: 100%;                  /* Figma: layoutSizing=FILL */
}

.header {
  display: flex;
  flex-direction: row;          /* Figma: layoutMode=HORIZONTAL */
  align-items: center;          /* Figma: counterAxisAlignItems=CENTER */
  justify-content: space-between; /* Figma: primaryAxisAlignItems=SPACE_BETWEEN */
  gap: 8px;                     /* Figma: itemSpacing=8 */
}
```

### Figma Auto Layout → Tailwind CSS（仅当项目使用 Tailwind 时）

| Figma 属性 | Tailwind Class |
|---|---|
| `layoutMode: HORIZONTAL` | `flex flex-row` |
| `layoutMode: VERTICAL` | `flex flex-col` |
| `primaryAxisAlignItems: MIN` | `justify-start` |
| `primaryAxisAlignItems: CENTER` | `justify-center` |
| `primaryAxisAlignItems: MAX` | `justify-end` |
| `primaryAxisAlignItems: SPACE_BETWEEN` | `justify-between` |
| `counterAxisAlignItems: MIN` | `items-start` |
| `counterAxisAlignItems: CENTER` | `items-center` |
| `counterAxisAlignItems: MAX` | `items-end` |
| `layoutSizing: HUG` | `w-fit` 或 `w-auto` |
| `layoutSizing: FILL` | `w-full` 或 `flex-1` |
| `itemSpacing: N` | `gap-[Npx]` |
| `paddingTop/Right/Bottom/Left` | `p-[T] [R] [B] [L]` |
| `layoutWrap: WRAP` | `flex-wrap` |

> **注意**：上表仅在项目已使用 Tailwind CSS 时适用。如果项目未使用 Tailwind，请使用通用 CSS 映射表。

### 绝对定位处理

```
如果节点使用绝对定位（position: absolute）：
1. 检查是否可以用 Flex/Grid 替代
2. 如果不能用 Flex/Grid 替代，保留 absolute 定位
3. 使用 Figma 的 x/y 坐标作为 top/left 值
4. 添加注释说明为什么使用绝对定位
```

## 样式生成规则

### 核心原则：尊重项目现有样式方案

```
样式生成优先级（从高到低）：
1. 项目已有的 Token/变量系统（如 figmaDesignTokens.ts、variables.less）
2. 项目已有的全局样式类（如 index.less 中的 utility classes）
3. 组件级样式文件（.less / .module.css / .module.scss）
4. Inline styles（仅用于动态计算的值）
5. Tailwind CSS（仅当项目已使用 Tailwind 时）
```

### Inline Styles（内联样式）

适用场景：简单组件、动态计算的样式值、一次性样式。

```tsx
// 内联样式仅用于动态计算的值
import React from 'react';

interface ProgressBarProps {
  /** 进度百分比，0-100 */
  progress: number;
}

export default function ProgressBar({ progress }: ProgressBarProps) {
  // 动态计算的宽度值，适合使用内联样式
  const barStyle: React.CSSProperties = {
    width: `${progress}%`,
    transition: 'width 0.3s ease',
  };

  return (
    <div className="progress-bar">
      <div className="progress-bar__fill" style={barStyle} />
    </div>
  );
}
```

### CSS Modules（.module.css / .module.less / .module.scss）

适用场景：组件级样式隔离，避免全局命名冲突。

```tsx
// Button.tsx — 使用 CSS Modules
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  children: React.ReactNode;
  onClick?: () => void;
}

export default function Button({ variant = 'primary', children, onClick }: ButtonProps) {
  return (
    <button className={`${styles.button} ${styles[variant]}`} onClick={onClick}>
      {children}
    </button>
  );
}
```

```css
/* Button.module.css */
.button {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.primary {
  background-color: var(--color-primary);
  color: #ffffff;
}

.secondary {
  background-color: var(--color-secondary);
  color: #333333;
}

.danger {
  background-color: var(--color-danger);
  color: #ffffff;
}
```

### Less / Sass

适用场景：全局样式、变量定义、mixin 复用、嵌套规则。

```less
// variables.less — 全局 Less 变量文件
// 从 Figma 设计 Token 中提取的颜色、间距、字体等变量

@color-primary: #1890ff;
@color-secondary: #595959;
@color-danger: #ff4d4f;
@color-bg: #ffffff;
@color-text: #333333;
@color-text-secondary: #666666;

@spacing-xs: 4px;
@spacing-sm: 8px;
@spacing-md: 16px;
@spacing-lg: 24px;
@spacing-xl: 32px;

@font-size-sm: 12px;
@font-size-base: 14px;
@font-size-lg: 16px;
@font-size-xl: 20px;

@border-radius-sm: 4px;
@border-radius-md: 6px;
@border-radius-lg: 8px;
```

```less
// mixins.less — 通用 Less mixin
// 封装常用的布局模式，减少重复代码

// Flex 居中布局（对应 Figma Auto Layout 的居中对齐）
.flex-center() {
  display: flex;
  align-items: center;
  justify-content: center;
}

// Flex 水平排列，两端对齐（对应 Figma layoutMode=HORIZONTAL + SPACE_BETWEEN）
.flex-between() {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

// 文本截断（单行）
.text-ellipsis() {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

```less
// Card.less — 组件级 Less 样式
@import '~@/styles/variables.less';
@import '~@/styles/mixins.less';

.card {
  padding: @spacing-lg;
  background-color: @color-bg;
  border-radius: @border-radius-md;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  &__header {
    .flex-between();
    margin-bottom: @spacing-md;
  }

  &__title {
    font-size: @font-size-xl;
    font-weight: 600;
    color: @color-text;
  }

  &__content {
    font-size: @font-size-base;
    color: @color-text-secondary;
    line-height: 1.6;
  }
}
```

### CSS Variables（Token 系统）

适用场景：主题切换、设计 Token 管理、跨组件样式一致性。

```css
/* tokens.css — 设计 Token 定义 */
/* 从 Figma 的 Design Tokens 中提取，保持与设计系统一致 */

:root {
  /* 颜色 Token */
  --color-primary: #1890ff;
  --color-primary-hover: #40a9ff;
  --color-primary-active: #096dd9;
  --color-secondary: #595959;
  --color-danger: #ff4d4f;
  --color-success: #52c41a;
  --color-warning: #faad14;

  /* 文字颜色 */
  --color-text-primary: #333333;
  --color-text-secondary: #666666;
  --color-text-disabled: #999999;
  --color-text-inverse: #ffffff;

  /* 背景颜色 */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f5f5f5;
  --color-bg-disabled: #f0f0f0;

  /* 间距 Token */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-xxl: 48px;

  /* 字体 Token */
  --font-size-xs: 12px;
  --font-size-sm: 13px;
  --font-size-base: 14px;
  --font-size-lg: 16px;
  --font-size-xl: 20px;
  --font-size-xxl: 24px;
  --font-size-display: 32px;

  /* 圆角 Token */
  --border-radius-sm: 4px;
  --border-radius-md: 6px;
  --border-radius-lg: 8px;
  --border-radius-full: 9999px;

  /* 阴影 Token */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
}
```

### Tailwind CSS（仅当项目已使用 Tailwind 时）

> **注意**：Tailwind CSS 仅作为样式方案之一，不作为默认选项。只有在项目已配置 Tailwind 时才使用。

```
Tailwind 样式生成优先级（仅当项目使用 Tailwind 时）：
1. Tailwind 内置 class（如 p-4, text-lg, bg-blue-500）
2. Tailwind 任意值（如 p-[18px], text-[13px], rounded-[6px]）
3. CSS 变量引用（如 text-[var(--color-primary)]）
4. 自定义 CSS（仅在无法用 Tailwind 表达时）
```

### 响应式处理

```
响应式策略（技术栈无关）：
1. 检查 Figma 中是否有多个尺寸变体（Desktop/Tablet/Mobile）
2. 如果有，为每个尺寸生成对应的样式规则
3. 如果没有，基于设计稿宽度推断响应式行为：
   - 宽度 > 1024px → 桌面布局
   - 宽度 768-1024px → 平板布局
   - 宽度 < 768px → 移动布局
4. 根据项目样式方案选择响应式写法：
   - Tailwind：sm:, md:, lg:, xl: 前缀
   - Less/Sass：使用 mixin 或媒体查询
   - CSS Modules：@media 规则
   - CSS Variables：container queries 或媒体查询
```

## Token 复用规则

### 检测项目中已有的 Token 文件

```
Token 文件检测流程：
1. 在项目根目录和 src/ 目录下搜索以下文件：
   - figmaDesignTokens.ts / figmaDesignTokens.js
   - tokens.ts / tokens.js / tokens.json
   - theme.ts / theme.js
   - design-tokens.ts / designTokens.ts
   - variables.less / _variables.scss / variables.css
2. 检查这些文件中是否已定义颜色、间距、字体、圆角等 Token
3. 记录 Token 的命名约定（camelCase / kebab-case / SCREAMING_SNAKE_CASE）
4. 记录 Token 的组织结构（按类别分组 / 扁平列表 / 嵌套对象）
```

### 验证现有 Token 与 Figma 设计的一致性

```
Token 一致性验证步骤：
1. 提取 Figma 设计中的所有颜色值、间距值、字体值
2. 与项目中已有 Token 进行逐一比对
3. 分类标记：
   - ✅ 已匹配：Figma 值在 Token 中已有对应定义
   - ⚠️ 近似匹配：Figma 值与 Token 值接近但不完全一致（如 #1890ff vs #1891ff）
   - ❌ 未匹配：Figma 值在 Token 中没有对应定义
4. 对于 ⚠️ 近似匹配：优先使用现有 Token，记录偏差供人工审核
5. 对于 ❌ 未匹配：评估是否需要新增 Token，而非直接硬编码
```

### "Validate, Don't Rebuild" 策略

```
核心原则：验证并复用现有 Token，而非重新创建。

操作步骤：
1. 生成代码前，先读取项目的 Token 文件
2. 将 Figma 设计值映射到最接近的已有 Token
3. 如果 Figma 使用了 Token 中不存在的值：
   a. 检查是否是设计偏差（如设计师使用了非标准颜色）
   b. 如果是合理的值，在 Token 文件中新增条目
   c. 如果是设计偏差，使用最接近的已有 Token 并添加注释
4. 生成的代码中只引用 Token 变量，不硬编码设计值
5. 在代码注释中标注使用的 Token 来源
```

### Token 文件的更新格式

```
Token 文件更新规则：
1. 保持与现有文件一致的格式（TypeScript 对象 / Less 变量 / CSS 变量）
2. 保持与现有文件一致的命名约定
3. 保持与现有文件一致的组织结构
4. 新增 Token 放在对应类别的末尾
5. 添加注释说明 Token 的来源和用途

示例 — 更新 TypeScript Token 文件：
```

```typescript
// figmaDesignTokens.ts — 设计 Token 定义
// 新增 Token 以 // [Figma] 开头注释

export const colors = {
  primary: '#1890ff',
  primaryHover: '#40a9ff',
  primaryActive: '#096dd9',
  secondary: '#595959',
  danger: '#ff4d4f',
  success: '#52c41a',
  warning: '#faad14',
  // [Figma] 新增：从 Figma 设计稿中提取的背景色
  backgroundTertiary: '#fafafa',
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  // [Figma] 新增：从 Figma 设计稿中提取的间距
  xxl: 48,
} as const;
```

```
示例 — 更新 Less Token 文件：
```

```less
// variables.less — 全局样式变量
// 新增变量以 // [Figma] 开头注释

// 颜色
@color-primary: #1890ff;
@color-primary-hover: #40a9ff;
@color-secondary: #595959;
@color-danger: #ff4d4f;
// [Figma] 新增：从 Figma 设计稿中提取的背景色
@color-bg-tertiary: #fafafa;

// 间距
@spacing-xs: 4px;
@spacing-sm: 8px;
@spacing-md: 16px;
@spacing-lg: 24px;
@spacing-xl: 32px;
// [Figma] 新增：从 Figma 设计稿中提取的间距
@spacing-xxl: 48px;
```

## 资产处理规则

### 图片

```
1. 使用 export_node_as_image 导出图片（TalkToFigma）
2. 保存到项目的 assets/images/ 目录
3. 使用 <img> 标签或 Next.js <Image> 组件引用
4. 添加 alt 属性（从 Figma 节点名称推断）
5. 设置正确的 width/height 属性
```

### SVG 图标

```
1. 使用 export_node_as_image(format: "SVG") 导出 SVG
2. 保存到项目的 assets/icons/ 目录
3. 创建 React/Vue 组件包装 SVG
4. 支持 currentColor 属性
5. 支持尺寸属性（width/height）
```

### 组件复用

```
1. 通过 get_local_components 获取 Figma 组件列表
2. 检查项目中是否已有对应的前端组件
3. 如果已有，直接复用，传入正确的 Props
4. 如果没有，创建新组件
```

## 代码质量规则

### 必须遵守

1. **TypeScript 优先**：所有组件使用 TypeScript，定义 Props 接口
2. **语义化 HTML**：使用 header/nav/main/section/article/footer
3. **可访问性**：添加 aria-label、role、alt 等属性
4. **组件单一职责**：每个组件只做一件事
5. **Props 可选**：合理使用可选 Props（?），提供默认值
6. **内联样式仅用于动态计算的值**：优先使用项目约定的样式方案（CSS Modules / Less / Sass / Tailwind 等），内联样式仅用于需要运行时动态计算的值（如进度条宽度、动态定位等）
7. **无魔法数字**：间距、颜色等使用 Token 或语义化 class

### 禁止事项

1. ❌ 不使用 Lorem ipsum 占位文本
2. ❌ 不使用 !important
3. ❌ 不滥用内联样式（仅限动态计算场景）
4. ❌ 不创建无意义的包装 div
5. ❌ 不硬编码颜色值（使用 Token）
6. ❌ 不使用 any 类型
7. ❌ 不生成未使用的导入

## 各技术栈代码模板

### React + Tailwind（仅当项目使用 Tailwind 时）

```tsx
// Button.tsx — React + Tailwind CSS 模板
// 仅在项目已配置 Tailwind CSS 时使用

interface ButtonProps {
  /** 按钮文字 */
  label: string;
  /** 按钮变体 */
  variant?: 'primary' | 'secondary';
  /** 点击回调 */
  onClick?: () => void;
}

export default function Button({ label, variant = 'primary', onClick }: ButtonProps) {
  // 根据变体选择对应的 Tailwind 样式
  const variantClass = variant === 'primary'
    ? 'bg-blue-500 text-white hover:bg-blue-600'
    : 'bg-gray-200 text-gray-700 hover:bg-gray-300';

  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded-md font-medium transition-colors ${variantClass}`}
    >
      {label}
    </button>
  );
}
```

### React + Less + Inline Styles

```tsx
// Card.tsx — React + Less + Inline Styles 模板
// 适用于使用 Less 预处理器，且部分样式需要动态计算的场景

import React from 'react';
import './Card.less';

interface CardProps {
  /** 卡片标题 */
  title: string;
  /** 卡片描述 */
  description?: string;
  /** 卡片封面图片 */
  coverUrl?: string;
  /** 自定义内边距（动态值，使用内联样式） */
  customPadding?: number;
}

export default function Card({ title, description, coverUrl, customPadding }: CardProps) {
  // 动态计算的值使用内联样式
  const dynamicStyle: React.CSSProperties = customPadding
    ? { padding: `${customPadding}px` }
    : {};

  return (
    <div className="card" style={dynamicStyle}>
      {/* 封面图片区域 */}
      {coverUrl && (
        <div className="card__cover">
          <img src={coverUrl} alt={title} className="card__image" />
        </div>
      )}

      {/* 卡片内容区域 */}
      <div className="card__body">
        <h3 className="card__title">{title}</h3>
        {description && (
          <p className="card__description">{description}</p>
        )}
      </div>
    </div>
  );
}
```

```less
// Card.less — 组件级 Less 样式
@import '~@/styles/variables.less';

.card {
  background-color: @color-bg;
  border-radius: @border-radius-md;
  box-shadow: @shadow-md;
  overflow: hidden;
  transition: box-shadow 0.2s ease;

  &:hover {
    box-shadow: @shadow-lg;
  }

  &__cover {
    width: 100%;
    height: 200px;
    overflow: hidden;
  }

  &__image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  &__body {
    padding: @spacing-md;
  }

  &__title {
    font-size: @font-size-lg;
    font-weight: 600;
    color: @color-text;
    margin-bottom: @spacing-sm;
  }

  &__description {
    font-size: @font-size-base;
    color: @color-text-secondary;
    line-height: 1.6;
  }
}
```

### React + CSS Modules

```tsx
// Modal.tsx — React + CSS Modules 模板
// 适用于使用 CSS Modules 进行样式隔离的项目

import React from 'react';
import styles from './Modal.module.css';

interface ModalProps {
  /** 是否显示弹窗 */
  visible: boolean;
  /** 弹窗标题 */
  title: string;
  /** 弹窗内容 */
  children: React.ReactNode;
  /** 关闭回调 */
  onClose: () => void;
}

export default function Modal({ visible, title, children, onClose }: ModalProps) {
  // 弹窗未显示时不渲染
  if (!visible) return null;

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        {/* 弹窗头部 */}
        <div className={styles.header}>
          <h2 className={styles.title}>{title}</h2>
          <button className={styles.closeBtn} onClick={onClose} aria-label="关闭">
            &times;
          </button>
        </div>

        {/* 弹窗内容 */}
        <div className={styles.body}>
          {children}
        </div>
      </div>
    </div>
  );
}
```

```css
/* Modal.module.css — CSS Modules 样式 */

.overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background-color: var(--color-bg-primary, #ffffff);
  border-radius: var(--border-radius-lg, 8px);
  box-shadow: var(--shadow-lg, 0 4px 16px rgba(0, 0, 0, 0.12));
  width: 100%;
  max-width: 520px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg, 24px);
  border-bottom: 1px solid #f0f0f0;
}

.title {
  font-size: var(--font-size-xl, 20px);
  font-weight: 600;
  color: var(--color-text-primary, #333333);
  margin: 0;
}

.closeBtn {
  border: none;
  background: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--color-text-secondary, #666666);
  padding: 4px 8px;
  border-radius: var(--border-radius-sm, 4px);
  transition: background-color 0.2s;
}

.closeBtn:hover {
  background-color: var(--color-bg-secondary, #f5f5f5);
}

.body {
  padding: var(--spacing-lg, 24px);
  overflow-y: auto;
}
```

### Vue 3 + Less

```vue
<!-- UserProfile.vue — Vue 3 + Less 模板 -->
<!-- 适用于使用 Vue 3 框架和 Less 预处理器的项目 -->

<template>
  <div class="user-profile">
    <!-- 用户头像区域 -->
    <div class="user-profile__avatar">
      <img
        :src="avatarUrl"
        :alt="`${userName} 的头像`"
        class="user-profile__image"
      />
    </div>

    <!-- 用户信息区域 -->
    <div class="user-profile__info">
      <h3 class="user-profile__name">{{ userName }}</h3>
      <p class="user-profile__role">{{ userRole }}</p>
    </div>

    <!-- 操作按钮区域 -->
    <div class="user-profile__actions">
      <button class="user-profile__btn user-profile__btn--primary" @click="$emit('follow')">
        关注
      </button>
      <button class="user-profile__btn user-profile__btn--secondary" @click="$emit('message')">
        私信
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
// 组件 Props 定义
interface Props {
  /** 用户头像地址 */
  avatarUrl: string;
  /** 用户名 */
  userName: string;
  /** 用户角色 */
  userRole?: string;
}

// 定义 Props 和事件
defineProps<Props>();
defineEmits<{
  follow: [];
  message: [];
}>();
</script>

<style lang="less" scoped>
@import '~@/styles/variables.less';

.user-profile {
  display: flex;
  align-items: center;
  gap: @spacing-md;
  padding: @spacing-md;
  background-color: @color-bg;
  border-radius: @border-radius-md;
  box-shadow: @shadow-sm;

  &__avatar {
    flex-shrink: 0;
  }

  &__image {
    width: 48px;
    height: 48px;
    border-radius: @border-radius-full;
    object-fit: cover;
  }

  &__info {
    flex: 1;
    min-width: 0; // 防止文本溢出容器
  }

  &__name {
    font-size: @font-size-base;
    font-weight: 600;
    color: @color-text;
    margin: 0 0 2px;
    .text-ellipsis(); // 使用全局 mixin
  }

  &__role {
    font-size: @font-size-sm;
    color: @color-text-secondary;
    margin: 0;
  }

  &__actions {
    display: flex;
    gap: @spacing-sm;
    flex-shrink: 0;
  }

  &__btn {
    padding: @spacing-xs @spacing-md;
    border-radius: @border-radius-sm;
    border: none;
    font-size: @font-size-sm;
    cursor: pointer;
    transition: all 0.2s;

    &--primary {
      background-color: @color-primary;
      color: #ffffff;

      &:hover {
        background-color: @color-primary-hover;
      }
    }

    &--secondary {
      background-color: @color-bg-secondary;
      color: @color-text;

      &:hover {
        background-color: darken(@color-bg-secondary, 5%);
      }
    }
  }
}
</style>
```

## TalkToFigma 工具使用

| 生成阶段 | 工具 | 用途 |
|---|---|---|
| 组件识别 | `get_local_components` | 获取 Figma 组件列表 |
| 资产导出 | `export_node_as_image` | 导出图片/SVG |
| 文本提取 | `scan_text_nodes` | 提取所有文本内容 |
| 节点详情 | `get_node_info` | 获取单个节点的精确属性 |
| 样式参考 | `get_styles` | 获取 Figma 样式定义 |
