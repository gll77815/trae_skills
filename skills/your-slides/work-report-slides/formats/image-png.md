# 输出格式 — 图片 PNG

把工作汇报渲染成静态 PNG。适合发 IM 群同步、嵌入 Notion/飞书文档、做内网公告头图。

## 适用场景

- 用户想发到企业微信/飞书/钉钉群（IM 不方便发 PPT 附件）
- 嵌入 Notion / 飞书云文档 / Confluence
- 做内网新闻/公告的配图
- 截图后发邮件给非 PPT 用户

## 不适用场景

- 听众要在 PPT 里继续编辑 → 用 PPTX 路径
- 内容会频繁更新（一改就要重新出图）→ 用 HTML 路径

## ⚠️ 关键限制条件

PNG 输出有两条路径，**都有限制**：

### 路径 A — HTML → 截图（首选）

先按 `html.md` 生成 HTML，再截图。

✅ 视觉最接近设计稿（CSS 阴影、状态灯渐变都能还原）
⚠️ **需要 Chrome MCP 或 headless 浏览器**：
- 用户启用 Claude in Chrome：`navigate` → `get_screenshot`
- 沙盒里有 chromium 可用 headless
- 两者都没有时走路径 B

### 路径 B — 直接生成 SVG → 转 PNG

用 Write 工具画 SVG，再用 ImageMagick/Pillow 转 PNG。

✅ 无浏览器依赖
⚠️ **视觉局限**：
- SVG 中文字体不同系统不一致
- 没有 CSS 高级特性（box-shadow、backdrop-blur 等）
- 复杂的表格/timeline 写 SVG 标签工作量大

## 实现要点

### 路径 A — HTML 截图

```bash
# 1. 先按 html.md 生成 weekly-report.html
# 2. headless chromium 截图
chromium --headless --disable-gpu \
  --screenshot=weekly-report.png \
  --window-size=960,540 \
  --hide-scrollbars \
  file:///path/to/weekly-report.html

# 或 Claude in Chrome:
# navigate(file:///path/to/weekly-report.html) → get_screenshot(selector=".slide")
```

⚠️ 调用 Chrome 前**先和用户确认**：

> 这步要 Chrome 来截图。我准备用 [Claude in Chrome / 沙盒 chromium]——可用吗？不行的话改用纯 SVG 路径。

### 路径 B — 纯 SVG（周报最小示例）

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" width="960" height="540">
  <rect width="960" height="540" fill="#FFFFFF"/>

  <!-- 主标题 -->
  <text x="24" y="48" font-size="28" font-weight="700" fill="#1F2937"
        font-family="-apple-system, 'PingFang SC', sans-serif">
    2026 W18 周报 · 产品工程组
  </text>

  <!-- 总状态灯 -->
  <circle cx="820" cy="40" r="6" fill="#22C55E"/>
  <text x="836" y="48" font-size="16" fill="#1F2937">整体绿灯</text>

  <!-- 三栏标题 -->
  <text x="24" y="120" font-size="18" font-weight="700" fill="#1F2937">✓ 上周完成</text>
  <text x="336" y="120" font-size="18" font-weight="700" fill="#1F2937">▶ 本周计划</text>
  <text x="648" y="120" font-size="18" font-weight="700" fill="#1F2937">⚠ 风险阻塞</text>

  <!-- 风险栏的状态灯+文字示例 -->
  <circle cx="652" cy="160" r="5" fill="#F59E0B"/>
  <text x="664" y="164" font-size="12" fill="#1F2937">A 上线后埋点数据缺失</text>

  <!-- 底部 KPI 行 -->
  <line x1="24" y1="490" x2="936" y2="490" stroke="#E5E7EB" stroke-width="1"/>
  <text x="24" y="514" font-size="14" fill="#1F2937">
    关键指标: DAU 1.2M ↑3% · 转化 2.4% 
  </text>
  <circle cx="488" cy="510" r="4" fill="#F59E0B"/>
  <text x="498" y="514" font-size="14" fill="#1F2937"> · 故障 1 </text>
  <circle cx="558" cy="510" r="4" fill="#EF4444"/>
</svg>
```

然后转 PNG：

```bash
convert -density 200 weekly-report.svg weekly-report.png
# 或
inkscape weekly-report.svg --export-png=weekly-report.png --export-dpi=200
```

### 状态灯在 SVG 里的实现

用 `<circle>`，半径 4-6px，对应颜色：

```xml
<circle cx="X" cy="Y" r="5" fill="#22C55E"/>  <!-- 绿 -->
<circle cx="X" cy="Y" r="5" fill="#F59E0B"/>  <!-- 黄 -->
<circle cx="X" cy="Y" r="5" fill="#EF4444"/>  <!-- 红 -->
<circle cx="X" cy="Y" r="5" fill="#94A3B8"/>  <!-- 灰 -->
```

**不要在 SVG 里用 emoji 🟢🟡🔴**，渲染依赖系统 emoji 字体，颜色和形状不可控。

### 表格在 SVG 里的实现

SVG 没有原生 table 标签，要用 `<rect>` 画背景 + `<line>` 画边框 + `<text>` 写内容。工作量大，**强烈建议月度复盘风格用路径 A（HTML 截图）**。

### 输出尺寸建议

| 用途 | 尺寸 |
|---|---|
| 通用预览/邮件正文 | 1920×1080（2× 960×540） |
| 企业微信/飞书群 | 1440×810（1.5×） |
| Notion/飞书内嵌 | 1920×1080 |
| 内网公告头图 | 1200×630（按平台要求调） |

## 验证清单

- [ ] 16:9 比例正确
- [ ] 状态灯颜色精准（路径 B 不用 emoji 检查通过）
- [ ] 中文字体正常显示（路径 B 在某些系统会出现方框）
- [ ] 文字清晰无锯齿（建议 2× 像素密度）
- [ ] 黄/红状态都有归因（不允许只有圆点）

## 用户拿到 PNG 后

- 拖进 IM 群发送
- 嵌入 Notion / 飞书 / 飞书云文档
- 加到邮件正文（不是附件，是内联图片）
- 内网公告/Wiki 头图

**不能编辑**：图片是栅格化的，想改文字要回头改源文件再重新导出。

⚠️ **不要承诺**：
- PNG 转 PPTX —— 工具链不可靠
- 自动适配不同比例（如 1:1 方图）—— 比例变了得重新设计布局
- 多页 PNG 合并成长图 —— 可以做（用 ImageMagick `convert -append`），但工作汇报场景不常用，需要用户明确要求
