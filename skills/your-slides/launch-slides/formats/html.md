# 输出格式 — HTML 单文件

把发布会页面渲染成一个独立的 HTML 文件，用浏览器打开即可看。

## 适用场景

- 用户要快速预览效果，不需要后续在 PPT 里编辑
- 想要做带动画、可交互的演示
- 要发链接给同事看（HTML 可以转 PDF 也可以直接发文件）

## 不适用场景

- 用户最终要在 PowerPoint 里继续编辑 → 改用 `pptx-office-mcp.md` 或 `pptx-standalone.md`
- 演讲场地只有 PPT 播放器 → 同上

## 限制条件

✅ **无外部依赖**：Claude 可以直接用 Write 工具生成，不需要任何 MCP 或第三方工具
✅ **完全自定义**：CSS/动画/字体能精确还原设计
⚠️ **字体回退**：用户机器上没装的字体会回退到默认，建议优先用系统字体或 Google Fonts CDN
⚠️ **不能直接转 PPT**：HTML 转 PPTX 工具链效果都不好，不要承诺这个

## 实现要点

### 基础结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>[金句]</title>
  <style>
    body { margin: 0; background: #0A0E1A; font-family: -apple-system, "PingFang SC", system-ui, sans-serif; }
    .slide {
      width: 960px; height: 540px;  /* 严格保持 16:9 */
      position: relative;
      margin: 40px auto;
      color: #fff;
      overflow: hidden;
    }
    /* 每个元素用 position: absolute + 风格 .md 里的 x/y 坐标 */
  </style>
</head>
<body>
  <div class="slide">
    <!-- 按对应 styles/*.md 的布局图放元素 -->
  </div>
</body>
</html>
```

### 坐标映射

- styles/*.md 里的坐标是 PPT 的 pt 单位（基准 960×540）
- 在 HTML 里 1pt ≈ 1px（不是严格相等但够用）
- 直接用 `position: absolute; top: 115px; left: 48px;` 还原

### 关键词换色

```html
<h1 class="hero">让方案
  <span style="color: #E0762D">穿透</span>到工序
</h1>
```

### 多页时

如果是"多页发布会序列"模式，每页是一个 `.slide` div，垂直堆叠，页与页之间留 40px。

### 文件位置

输出到用户的工作目录（如 outputs/ 或用户指定的文件夹），文件名用金句的关键词，比如 `穿透工序-launch-slides.html`。

## 验证清单（生成后必过）

- [ ] 浏览器打开后 16:9 比例不变形（如果用户屏幕窄会出现横向滚动条但不影响打印/截图）
- [ ] 巨幅金句未被截断
- [ ] 留白比例符合对应风格的要求（苹果式上下 ≥60px）
- [ ] 关键词换色生效（不是全行同色）
- [ ] 用 Chrome 打开 → 打印预览检查能否清晰输出 PDF（A4 横向）

## 用户拿到文件后怎么用

告诉用户：

> 1. 双击 HTML 打开浏览器查看
> 2. 想转 PDF：浏览器 Ctrl+P → 选"保存为 PDF" → 横向、无边距
> 3. 想要截图：F12 → 选 .slide 元素 → 右键 → "Capture node screenshot"

不要承诺 HTML 能转 PPTX，工具链都不可靠。
