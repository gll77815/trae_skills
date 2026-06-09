# 浏览器验证引擎规范

## 概述

浏览器验证引擎通过 `integrated_browser` MCP 工具，对生成的前端代码进行渲染验证和像素级对比校验。它不是简单地"看截图"，而是通过 DOM/CSS 精确对比来发现偏差。

## 验证流程

### Step 1: 渲染验证

**目标：** 确认代码能正确编译和渲染

1. 启动本地开发服务器
   ```bash
   npm run dev  # 或用户项目的启动命令
   ```
2. 使用 `browser_navigate` 打开页面
3. 使用 `browser_wait_for` 等待页面完全加载
4. 使用 `browser_console_messages` 检查是否有错误
5. 使用 `browser_take_screenshot` 截取初始渲染结果

### Step 2: DOM/CSS 精确对比

**目标：** 逐元素对比 CSS 计算值与设计 Token

**使用 `browser_evaluate` 提取关键元素的 CSS 属性：**

```javascript
// 提取指定元素的完整 CSS 计算值
const element = document.querySelector('[data-testid="header"]');
if (!element) return 'Element not found';

const style = getComputedStyle(element);
return JSON.stringify({
  // 布局属性
  display: style.display,
  flexDirection: style.flexDirection,
  alignItems: style.alignItems,
  justifyContent: style.justifyContent,
  gap: style.gap,
  position: style.position,

  // 盒模型
  width: style.width,
  height: style.height,
  minWidth: style.minWidth,
  maxWidth: style.maxWidth,
  paddingTop: style.paddingTop,
  paddingRight: style.paddingRight,
  paddingBottom: style.paddingBottom,
  paddingLeft: style.paddingLeft,
  marginTop: style.marginTop,
  marginRight: style.marginRight,
  marginBottom: style.marginBottom,
  marginLeft: style.marginLeft,

  // 视觉属性
  backgroundColor: style.backgroundColor,
  color: style.color,
  borderColor: style.borderColor,
  borderWidth: style.borderWidth,
  borderRadius: style.borderRadius,
  boxShadow: style.boxShadow,
  opacity: style.opacity,

  // 字体属性
  fontSize: style.fontSize,
  fontWeight: style.fontWeight,
  fontFamily: style.fontFamily,
  lineHeight: style.lineHeight,
  letterSpacing: style.letterSpacing,
  textAlign: style.textAlign,

  // 其他
  overflow: style.overflow,
  cursor: style.cursor,
  transition: style.transition
}, null, 2);
```

**对比策略：**

| 属性类别 | 对比方法 | 容差 |
|---|---|---|
| 颜色 | RGB 各分量差值 ≤ 5 | ΔE < 2 |
| 间距（padding/margin/gap） | 数值差值 ≤ 1px | 1px |
| 尺寸（width/height） | 数值差值 ≤ 1px | 1px |
| 字号 | 数值差值 ≤ 1px | 1px |
| 字重 | 完全一致 | 0 |
| 圆角 | 数值差值 ≤ 1px | 1px |
| 布局方向 | 完全一致 | 0 |
| 对齐方式 | 完全一致 | 0 |

### Step 3: 像素级视觉对比

**目标：** 通过截图对比发现整体视觉偏差

1. 使用 `export_node_as_image` 导出 Figma 设计稿截图（TalkToFigma）
2. 使用 `browser_take_screenshot` 截取浏览器渲染结果
3. 使用 `browser_evaluate` 进行像素对比分析：

```javascript
// 获取页面关键区域的视觉信息
const regions = document.querySelectorAll('[data-figma-node]');
return JSON.stringify(Array.from(regions).map(el => {
  const rect = el.getBoundingClientRect();
  const style = getComputedStyle(el);
  return {
    nodeId: el.dataset.figmaNode,
    bounds: {
      x: Math.round(rect.x),
      y: Math.round(rect.y),
      width: Math.round(rect.width),
      height: Math.round(rect.height)
    },
    backgroundColor: style.backgroundColor,
    textColor: style.color,
    fontSize: style.fontSize
  };
}));
```

**差异分析维度：**

| 维度 | 检查内容 | 严重程度 |
|---|---|---|
| 颜色偏差 | 背景色、文字色、边框色 | 🔴 高 |
| 间距偏差 | padding、margin、gap | 🔴 高 |
| 尺寸偏差 | width、height | 🟡 中 |
| 对齐偏差 | 元素水平/垂直对齐 | 🟡 中 |
| 字体偏差 | 字号、字重、行高 | 🔴 高 |
| 圆角偏差 | border-radius | 🟢 低 |
| 阴影偏差 | box-shadow | 🟢 低 |

### Step 4: 自动修复

**目标：** 根据差异报告自动修正代码

**修复策略：**

```
1. 颜色偏差 → 修正 CSS 变量或 Tailwind class
2. 间距偏差 → 调整 padding/margin/gap 值
3. 尺寸偏差 → 调整 width/height 或 flex 属性
4. 对齐偏差 → 调整 align-items/justify-content
5. 字体偏差 → 修正 font-size/font-weight/line-height
6. 布局偏差 → 检查 display/flex-direction 是否正确
```

**修复循环：**
```
修复代码 → 重新渲染 → 重新对比 → 如果仍有偏差 → 继续修复
最大迭代次数：3 次
如果 3 次后仍有偏差 → 生成差异报告，提示人工介入
```

## 差异报告格式

当验证完成或达到最大迭代次数时，生成差异报告：

```markdown
## 像素级验证报告

### 总体评分：92/100

### 通过项 ✅
- 颜色还原：所有颜色偏差 ΔE < 2
- 字体还原：字号、字重完全一致
- 组件结构：与 Figma 组件一一对应

### 偏差项 ⚠️
| 元素 | 属性 | 设计值 | 实际值 | 偏差 |
|---|---|---|---|---|
| Header | padding-top | 16px | 15px | 1px |
| Card | gap | 12px | 14px | 2px |
| Button | border-radius | 8px | 6px | 2px |

### 建议
- Card 的 gap 值建议从 14px 调整为 12px
- Button 的 border-radius 建议从 6px 调整为 8px
```

## 浏览器工具使用指南

| 验证阶段 | 工具 | 用途 |
|---|---|---|
| 页面加载 | `browser_navigate` | 打开目标页面 |
| 等待渲染 | `browser_wait_for` | 等待元素出现 |
| DOM 结构 | `browser_snapshot` | 获取 DOM 树 |
| CSS 提取 | `browser_evaluate` | 执行 JS 提取计算样式 |
| 视觉截图 | `browser_take_screenshot` | 截取渲染结果 |
| 滚动检查 | `browser_scroll` | 检查溢出/滚动行为 |
| 响应式检查 | `browser_evaluate` | 修改 viewport 宽度 |
| 控制台检查 | `browser_console_messages` | 检查 JS 错误 |
| 网络检查 | `browser_network_requests` | 检查资源加载 |

## 注意事项

1. **先编译再验证**：确保代码无编译错误后再进行浏览器验证
2. **使用 data-testid**：为关键元素添加 `data-testid` 和 `data-figma-node` 属性，方便定位
3. **等待渲染完成**：字体加载、图片加载需要时间，使用 `browser_wait_for` 确保完全渲染
4. **考虑浏览器差异**：不同浏览器的渲染可能有细微差异，以 Chrome 为基准
5. **不要过度优化**：1px 以内的偏差在大多数场景下可以接受
