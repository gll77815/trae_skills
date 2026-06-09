# 输出格式 — HTML 单文件

把工作汇报渲染成独立 HTML，用浏览器打开即可看。

## 适用场景

- 用户想做"活看板"：嵌进 Notion/飞书或挂内网，每周更新数字就行
- 周会前快速预览，不用打开 PPT
- 想保留交互（点击展开附录、可折叠的归因说明）

## 不适用场景

- 听众会议室只能放 PPT → 改用 `pptx-office-mcp.md` 或 `pptx-standalone.md`
- 听众要求"邮件附件，能离线打开"——HTML 也可以，但 PPTX 更符合工作汇报的"邮件习惯"

## 限制条件

✅ **无外部依赖**：Claude 用 Write 工具直接生成，无需任何 MCP
✅ **状态灯/表格/timeline 用 CSS 都能精确还原**
⚠️ **字体回退**：用户没装的字体会回退，建议优先用系统字体（`-apple-system, "PingFang SC", "Microsoft YaHei"`）
⚠️ **不能直接转 PPTX**：HTML 转 PPTX 工具链不可靠，不要承诺

## 实现要点

### 基础结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>2026 W18 周报</title>
  <style>
    body {
      margin: 0; background: #f8fafc;
      font-family: -apple-system, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
      color: #1f2937;
    }
    .slide {
      width: 960px; height: 540px;  /* 严格 16:9 */
      position: relative;
      margin: 40px auto;
      background: #fff;
      box-shadow: 0 4px 12px rgba(0,0,0,0.06);
      overflow: hidden;
    }
    /* 状态灯统一样式 */
    .light { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }
    .light-green { background: #22C55E; }
    .light-yellow { background: #F59E0B; }
    .light-red { background: #EF4444; }
    .light-gray { background: #94A3B8; }
  </style>
</head>
<body>
  <div class="slide">
    <!-- 按对应 styles/*.md 的布局图放元素 -->
  </div>
</body>
</html>
```

### 状态灯实现

工作汇报最常用的视觉元素就是状态灯，**全文统一一个 CSS class**：

```html
<span class="light light-yellow"></span>付费转化 2.4%
```

### 表格实现（月度复盘风格）

```html
<table style="width: 100%; border-collapse: collapse; font-size: 13pt;">
  <thead style="background: #F1F5F9; color: #475569;">
    <tr>
      <th style="padding: 8px 12px; text-align: left;">指标</th>
      <th style="padding: 8px 12px;">目标</th>
      <th style="padding: 8px 12px;">实际</th>
      <th style="padding: 8px 12px;">状态</th>
      <th style="padding: 8px 12px; text-align: left;">偏差归因</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #E5E7EB;">
      <td style="padding: 8px 12px;">DAU</td>
      <td style="padding: 8px 12px;">1.2M</td>
      <td style="padding: 8px 12px;">1.25M</td>
      <td style="padding: 8px 12px;"><span class="light light-green"></span></td>
      <td style="padding: 8px 12px; color: #6B7280;">-</td>
    </tr>
  </tbody>
</table>
```

### Timeline 实现（项目里程碑风格）

```html
<div style="position: relative; height: 80px; margin: 60px 40px;">
  <!-- 主线 -->
  <div style="position: absolute; top: 12px; left: 0; right: 0; height: 2px; background: #E5E7EB;"></div>
  <!-- 节点 -->
  <div style="position: absolute; left: 0;"><span class="light" style="width: 14px; height: 14px; background: #22C55E;"></span></div>
  <div style="position: absolute; left: 25%;"><span class="light" style="width: 14px; height: 14px; background: #22C55E;"></span></div>
  <div style="position: absolute; left: 50%;"><span class="light" style="width: 14px; height: 14px; background: #F59E0B;"></span></div>
  <!-- ... -->
</div>
```

### 多页时

如果用户选了"多页汇报序列"，每页一个 `.slide` div 垂直堆叠，页间 40px。也可以做成"标签页"形式（带顶部 tab 切换），但默认垂直堆叠更稳。

### 文件位置

输出到用户工作目录（outputs/ 或用户指定），文件名格式：`2026-W18-周报.html` / `2026-05-月度复盘.html`。

## 验证清单（生成后必过）

- [ ] 浏览器打开 16:9 比例不变形
- [ ] 状态灯颜色与全局规范一致（不要出现自创色）
- [ ] 表格行高足够（≥32px），不挤
- [ ] 黄/红状态都有归因（不允许空着 "-"）
- [ ] 行动项都含责任人+deadline
- [ ] 中文字体显示正常（用 Chrome / Safari / Edge 各开一次确认）

## 用户拿到文件后

告诉用户：

> 1. 双击 HTML 用浏览器打开
> 2. 想发邮件：直接附件 .html 文件，对方双击就能看
> 3. 想转 PDF：Ctrl+P → "保存为 PDF" → 横向、无边距
> 4. 想嵌入 Notion/飞书：复制内容粘贴（会自动转格式），或上传文件

**不要承诺**：
- HTML 转 PPTX —— 工具链不可靠
- 邮件客户端直接预览 HTML —— 大多数邮件客户端会把附件 HTML 当成代码而不是网页
