# 输出格式 — PPTX via Office MCP（在用户打开的 PowerPoint 里实时改）

直接在用户当前打开的 PowerPoint 窗口里 duplicate / 编辑 / 替换。**工作汇报最常用的路径**——大多数公司周会/月会都用 PPT。

## 适用场景

- 用户已打开周报/月报的 .pptx 文件
- 用户想在原 PPT 模板（公司模板）里只换内容
- 用户在会议中临场调整某页

## ⚠️ 关键限制条件（必须告知用户）

调用 Office MCP 工具前**先确认**三件事：

1. **用户机器是 Mac/Windows 装了 PowerPoint**（iPad/Web 版 PPT 不支持 Office MCP）
2. **用户已在 Claude 启用 Office MCP 连接**
3. **目标 .pptx 文件当前处于打开状态**

如果不满足，提示用户：

> 改 PPTX 文件本身需要：① 装 PowerPoint；② 启用 Office MCP；③ 目标文件处于打开状态。
> 如果暂时不方便，我可以改用「PPTX 独立生成」（生成新文件不依赖 MCP）或「HTML 单文件」（最快，浏览器看）——选哪个？

## 实现要点

### Step 1 — 背景策略

**复用模板**（用户选了"复用现有模板"，工作汇报场景常用）：

```js
// 1. duplicate 已有的周报/月报某页（用户的公司模板）
// 2. execute_office_js 列出 shapes
slide.shapes.load("items/id,items/name,items/top,items/left");
await context.sync();
// 3. 保留背景/页眉/页脚 shape（通常 id 较小,如 8/29/81）
// 4. 删除中间内容区的旧元素
```

**纯白底背景**（用户选了"白底"，工作汇报默认）：

```js
const newSlide = slides.add(SlideLayoutType.titleOnly);
newSlide.background.fill.setSolidFill({color: "#FFFFFF"});
```

### Step 2 — 创建状态灯（工作汇报的标志元素）

状态灯用 `addGeometricShape("Oval")`，每个状态灯 8-10pt 直径，颜色严格按全局规范：

```js
const light = shapes.addGeometricShape("Oval");
light.geometricShapeType = "Oval";
light.left = 100;
light.top = 200;
light.width = 10;  // 10pt 直径
light.height = 10;
light.fill.setSolidFill({color: "22C55E"});  // 绿
light.lineFormat.visible = false;  // 关掉边框
```

⚠️ **不要用 emoji 🟢🟡🔴 代替**——emoji 在不同字体回退下颜色可能漂移，统一用 shape 控制颜色最稳。

### Step 3 — 表格（月度复盘必用）

PowerPoint 表格用 `slide.shapes.addTable(rowCount, columnCount, ...)`：

```js
const table = slide.shapes.addTable(5, 5, {
  left: 24, top: 230, width: 912, height: 200
});
// 设置表头样式
const headerRow = table.rows.getItemAt(0);
headerRow.cells.items.forEach(cell => {
  cell.shape.fill.setSolidFill({color: "F1F5F9"});
  // 表头文字 bold + 14pt
});
// 设置数据行...
```

或者用 `addTextBox` 模拟表格（更灵活，可以精确控制对齐和状态灯位置）：每个 cell 一个 textbox，状态列单独放一个 Oval shape。

### Step 4 — 富文本批量写入

工作汇报通常没有"金句换色"那种富文本，但有 BLUF 加粗、状态灯文字、责任人/时间标签的字体大小差异。**用单次 `edit_slide_xml` 批量写**：

```xml
<a:p>
  <a:r>
    <a:rPr lang="zh-CN" sz="3600" b="1">
      <a:solidFill><a:srgbClr val="1F2937"/></a:solidFill>
      <a:latin typeface="+mj-lt"/>
      <a:ea typeface="+mj-ea"/>
    </a:rPr>
    <a:t>上周整体绿灯,但 A 项目需本周拍板</a:t>
  </a:r>
</a:p>
```

注意：
- 字号 1/100 pt（36pt → `sz="3600"`）
- `<a:t>` 内的 `&` 必须 escape 成 `&amp;`
- 工作汇报字号比发布会小一档：BLUF 32-36pt（不像发布会 48-72pt），正文 12-14pt

### Step 5 — autosize 必填

`edit_slide_xml` 必须传 `autosize_shape_ids` 数组。

### Step 6 — 状态灯统一规范的实现注意

调用前在代码里定义一个映射：

```js
const STATUS_COLORS = {
  green:  "22C55E",
  yellow: "F59E0B",
  red:    "EF4444",
  gray:   "94A3B8"
};
```

整页所有状态灯都从这个映射取色，**禁止局部覆盖**。

## 验证清单

调一次 `verify_slide_visual`，特别检查：

- [ ] 状态灯颜色与全局规范一致（全页一个口径）
- [ ] 黄/红状态都有归因文字（如果只有圆点没文字，说明漏了）
- [ ] 行动项都含责任人 + deadline
- [ ] BLUF 字号是不是页面最显眼元素（向上汇报风格）
- [ ] 表格行高足够（≥32pt）
- [ ] 底栏没被裁切（y + height > 540 是常见问题）

发现问题改原元素位置/字号，不要删了重建。

## Done 判断

`verify_slide_visual` 返回 no significant issues，且用户在新页面上明确说"满意/可以/OK"。

## 工作汇报场景的临场调整 tips

会议进行中老板可能要求"把 A 项目状态从黄改红"或"加一条 ask"，Office MCP 路径最适合这种场景：

- 改状态灯：找到对应 Oval shape，改 fill color，**不要重建**
- 加一条 ask：在底部 textbox 末尾追加一行，autosize 自动调整高度
- 删除附录页：`slides.getItemAt(N).delete()`

⚠️ 临场调整也要**先 duplicate 一份**（除非用户明确说"直接改，时间紧"），避免会后老板想看上一版本时回不去。
