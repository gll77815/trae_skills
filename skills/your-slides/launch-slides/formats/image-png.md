# 输出格式 — 图片 PNG

把发布会页面渲染成静态 PNG 图片。用于头图、海报、社交分享、嵌入到其他文档。

## 适用场景

- 用户想要发到微信/小红书等社交平台的成品图
- 想做公众号/邮件的头图
- 想嵌入到 Word / Notion / 飞书文档里
- 不需要"可编辑性"

## ⚠️ 关键限制条件

PNG 输出有两条技术路径，**两条都有限制**：

### 路径 A — HTML → 截图（首选）

先按 `html.md` 生成 HTML，然后截图。

✅ 视觉效果最接近设计稿（动画/阴影/混合模式都能还原）
⚠️ **需要 Chrome MCP 或 headless 浏览器**：
  - 如果用户启用了 Claude in Chrome，可以 `navigate` → `get_screenshot`
  - 如果环境里有 sandbox bash 的 chromium，可以 headless 截图
  - **如果两者都没有**，这条路走不通，要切到路径 B

### 路径 B — 直接生成 SVG

用 Write 工具直接画一个 SVG，再转 PNG（用 ImageMagick / Pillow 等）。

✅ 不依赖任何浏览器或 MCP，纯文件生成
⚠️ **视觉局限**：
  - SVG 文字渲染在不同系统上字体不一致
  - 没有 CSS 高级特性（filter、backdrop-blur 等）
  - 复杂动画/渐变需要手写 SVG 标签，工作量大

## 实现要点

### 路径 A — HTML 截图

```bash
# 1. 先按 html.md 生成 launch.html
# 2. 用 headless Chrome 截图(如果可用)
chromium --headless --disable-gpu \
  --screenshot=launch.png \
  --window-size=960,540 \
  file:///path/to/launch.html

# 或者通过 Claude in Chrome 工具:
# navigate → get_screenshot(selector=".slide")
```

⚠️ 调用 Chrome 前**先和用户确认**：

> 这一步需要 Chrome 来截图。我准备用 [Claude in Chrome / 沙盒里的 chromium]——确认可用吗？如果环境里没有，我可以改用直接生成 SVG 的路径。

### 路径 B — 纯 SVG

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" width="960" height="540">
  <rect width="960" height="540" fill="#0A0E1A"/>

  <text x="48" y="36" font-size="14" fill="#E0762D" letter-spacing="2">
    产品价值 · PRODUCT VALUE
  </text>

  <text x="48" y="160" font-size="48" font-weight="700" fill="#FFFFFF">
    让方案
    <tspan fill="#E0762D">穿透</tspan>
    到工序
  </text>

  <!-- 价值点四列循环 -->
  <g font-family="-apple-system, 'PingFang SC', sans-serif">
    <g transform="translate(48, 360)">
      <text font-size="28" fill="#E0762D">01</text>
      <text y="28" font-size="20" font-weight="700" fill="#FFFFFF">穿透工序</text>
      <text y="64" font-size="12" fill="#9CB3CC">方案触发二次交底</text>
    </g>
    <!-- ...另外三列 transform=translate(264,...) (480,...) (696,...) -->
  </g>
</svg>
```

然后转 PNG：

```bash
# 用 ImageMagick
convert -density 200 launch.svg launch.png
# 或者用 inkscape
inkscape launch.svg --export-png=launch.png --export-dpi=200
```

### 输出尺寸建议

| 用途 | 尺寸 |
|---|---|
| 通用预览 | 1920×1080（2× of 960×540） |
| 微信公众号头图 | 900×383 |
| 小红书封面 | 1242×1660（要重新设计 4:3 竖版） |
| 嵌入 Word/Notion | 1920×1080 PNG |

## 验证清单

- [ ] 16:9 比例正确（或用户指定的其他比例）
- [ ] 中文字体没有显示成方框（路径 B 在某些系统会出现）
- [ ] 文字清晰，无锯齿（建议 2× 像素密度）
- [ ] 颜色与设计稿一致（路径 A 通常更准，路径 B 偶有色差）

## 用户拿到图片后

- 直接双击查看
- 拖进微信/邮件/文档
- **不能编辑**：图片是栅格化的，想改文字得回头改源文件再重新导出

⚠️ **不要承诺**：
- PNG 转 PPTX —— 工具链不可靠
- 自动适配不同尺寸 —— 不同比例需要重新设计布局，不是简单缩放
