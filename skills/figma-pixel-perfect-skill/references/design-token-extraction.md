# 设计 Token 提取规范

## 概述

设计 Token 是设计系统中最基础的视觉原子。本规范定义了如何从 Figma 设计数据中精确提取所有 Token，确保生成的代码在视觉上与设计稿完全一致。

## Token 分类与提取规则

### 1. 颜色 Token

**提取来源：** 节点的 `fills`、`strokes`、`background` 属性

| Token 名称 | Figma 属性 | 提取规则 | 输出格式 |
|---|---|---|---|
| 背景色 | `fills[0].color` | RGBA → HEX | `#RRGGBB` 或 `#RRGGBBAA` |
| 文字色 | `fills[0].color`（TextNode） | RGBA → HEX | `#RRGGBB` |
| 描边色 | `strokes[0].color` | RGBA → HEX | `#RRGGBB` |
| 渐变色 | `fills[].gradientStops` | 逐个提取 | `linear-gradient(...)` |

**RGBA → HEX 转换规则：**
```
R: Math.round(color.r * 255).toString(16).padStart(2, '0')
G: Math.round(color.g * 255).toString(16).padStart(2, '0')
B: Math.round(color.b * 255).toString(16).padStart(2, '0')
A: Math.round(color.a * 255).toString(16).padStart(2, '0')

如果 A === 'ff'，输出 #RRGGBB（6位）
如果 A !== 'ff'，输出 #RRGGBBAA（8位）
```

### 2. 字体 Token

**提取来源：** TextNode 的 `style` 属性

| Token 名称 | Figma 属性 | 精度要求 | Tailwind 映射 |
|---|---|---|---|
| 字体族 | `style.fontFamily` | 完全一致 | `font-[family]` |
| 字号 | `style.fontSize` | 精确到 px | `text-[Npx]` |
| 字重 | `style.fontWeight` | 完全一致 | `font-[N]` |
| 行高 | `style.lineHeightPx` | 精确到 px | `leading-[Npx]` |
| 字间距 | `style.letterSpacing` | 精确到 0.1px | `tracking-[N]` |
| 文本对齐 | `style.textAlignHorizontal` | 完全一致 | `text-left/center/right` |
| 文本装饰 | `style.textDecoration` | 完全一致 | `underline/line-through/none` |
| 文本转换 | `style.textCase` | 完全一致 | `uppercase/lowercase/capitalize` |

**字号映射建议（Figma px → Tailwind class）：**
```
10px → text-[10px]
12px → text-xs (12px)
14px → text-sm (14px)
16px → text-base (16px)
18px → text-lg (18px)
20px → text-xl (20px)
24px → text-2xl (24px)
30px → text-3xl (30px)
36px → text-4xl (36px)
其他 → text-[Npx]
```

### 3. 间距 Token

**提取来源：** FrameNode 的布局属性

| Token 名称 | Figma 属性 | 精度要求 | Tailwind 映射 |
|---|---|---|---|
| 上内边距 | `paddingTop` | 精确到 px | `pt-[Npx]` |
| 右内边距 | `paddingRight` | 精确到 px | `pr-[Npx]` |
| 下内边距 | `paddingBottom` | 精确到 px | `pb-[Npx]` |
| 左内边距 | `paddingLeft` | 精确到 px | `pl-[Npx]` |
| 元素间距 | `itemSpacing` | 精确到 px | `gap-[Npx]` |
| 交叉轴间距 | `counterAxisSpacing` | 精确到 px | `gap-y-[Npx]` |

**间距映射建议（Figma px → Tailwind class）：**
```
4px → p-1 (4px)
8px → p-2 (8px)
12px → p-3 (12px)
16px → p-4 (16px)
20px → p-5 (20px)
24px → p-6 (24px)
32px → p-8 (32px)
40px → p-10 (40px)
48px → p-12 (48px)
64px → p-16 (64px)
其他 → p-[Npx]
```

### 4. 圆角 Token

**提取来源：** 节点的 `cornerRadius` 属性

| Token 名称 | Figma 属性 | 精度要求 | Tailwind 映射 |
|---|---|---|---|
| 统一圆角 | `cornerRadius` | 精确到 px | `rounded-[Npx]` |
| 独立圆角 | `topLeftRadius` 等 | 精确到 px | `rounded-tl-[Npx]` 等 |

**圆角映射建议：**
```
0px → rounded-none
2px → rounded-sm (2px)
4px → rounded (4px)
6px → rounded-md (6px)
8px → rounded-lg (8px)
12px → rounded-xl (12px)
16px → rounded-2xl (16px)
9999px → rounded-full
其他 → rounded-[Npx]
```

### 5. 阴影 Token

**提取来源：** 节点的 `effects` 数组中 `type === "DROP_SHADOW"` 的项

| Token 名称 | Figma 属性 | 精度要求 |
|---|---|---|
| 阴影 X 偏移 | `effect.offset.x` | 精确到 px |
| 阴影 Y 偏移 | `effect.offset.y` | 精确到 px |
| 阴影模糊 | `effect.radius` | 精确到 px |
| 阴影扩散 | `effect.spread` | 精确到 px |
| 阴影颜色 | `effect.color` | RGBA → HEX |

**输出格式：**
```
box-shadow: Xpx Ypx blurpx spreadpx #RRGGBBAA
```

### 6. 边框 Token

**提取来源：** 节点的 `strokes` 和 `strokeWeight` 属性

| Token 名称 | Figma 属性 | 精度要求 |
|---|---|---|
| 边框宽度 | `strokeWeight` | 精确到 px |
| 边框颜色 | `strokes[0].color` | RGBA → HEX |
| 边框样式 | `strokeAlign` | solid/dashed（Figma 不支持 dotted） |

### 7. 尺寸 Token

**提取来源：** 节点的 `width`、`height`、`minWidth`、`maxWidth` 等

| Token 名称 | Figma 属性 | 精度要求 |
|---|---|---|
| 宽度 | `width` | 精确到 px |
| 高度 | `height` | 精确到 px |
| 最小宽度 | `minWidth` | 精确到 px |
| 最大宽度 | `maxWidth` | 精确到 px |
| 宽度模式 | `layoutSizingHorizontal` | FIXED/HUG/FILL |
| 高度模式 | `layoutSizingVertical` | FIXED/HUG/FILL |

### 8. 透明度 Token

**提取来源：** 节点的 `opacity` 属性

| Token 名称 | Figma 属性 | 精度要求 |
|---|---|---|
| 不透明度 | `opacity` | 精确到小数点后 2 位 |

## Token 输出格式

提取完成后，生成结构化的 Token 文件：

### CSS 变量格式（推荐）
```css
:root {
  /* 颜色 */
  --color-primary: #3B82F6;
  --color-secondary: #10B981;
  --color-background: #FFFFFF;
  --color-text: #1F2937;
  --color-border: #E5E7EB;

  /* 字体 */
  --font-family: 'Inter', sans-serif;
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 20px;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;

  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-lg: 16px;
  --spacing-xl: 24px;
  --spacing-2xl: 32px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* 阴影 */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

### Tailwind 配置格式
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
      },
      fontSize: {
        'display': ['36px', { lineHeight: '1.1' }],
        'title': ['24px', { lineHeight: '1.3' }],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07)',
      }
    }
  }
}
```

## TalkToFigma 工具使用

| Token 类别 | 主要工具 | 辅助工具 |
|---|---|---|
| 颜色 | `read_my_design` | `get_node_info` |
| 字体 | `read_my_design` | `scan_text_nodes` |
| 间距 | `read_my_design` | `get_node_info` |
| 圆角 | `read_my_design` | `get_node_info` |
| 阴影 | `read_my_design` | `get_node_info` |
| 边框 | `read_my_design` | `get_node_info` |
| 尺寸 | `read_my_design` | `get_node_info` |
| 透明度 | `read_my_design` | `get_node_info` |
| 样式变量 | `get_styles` | — |

## 注意事项

1. **精度优先**：所有数值精确到 px，不要四舍五入
2. **颜色格式统一**：统一使用 HEX 格式，不使用 RGB/HSL
3. **Figma 颜色空间**：Figma 使用 sRGB，注意与 P3 等色彩空间的转换
4. **字体回退**：如果 Figma 中的字体在 Web 中不可用，提供合理的回退字体
5. **Token 命名**：使用语义化命名（如 `color-primary`），而非视觉命名（如 `color-blue-500`）
