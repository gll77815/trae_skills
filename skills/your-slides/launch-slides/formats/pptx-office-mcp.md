# 输出格式 — PPTX via Office MCP（在用户打开的 PowerPoint 里实时改）

直接在用户当前打开的 PowerPoint 窗口里 duplicate / 编辑 / 替换形状。改完用户回到 PPT 就能看到。

## 适用场景

- 用户已经打开一个具体 .pptx 文件，要改其中一页或加几页
- 用户希望"保留原模板的标题栏/底栏/背景图"，只重做中间内容
- 用户机器上装了 PowerPoint 且 Office MCP 已连接

## ⚠️ 关键限制条件（必须告知用户）

调用 Office MCP 工具前，**先和用户确认**这三件事：

1. **用户机器是 Mac/Windows 装了 PowerPoint**——iPad/Web 版的 PPT 不支持 Office MCP
2. **用户已在 Claude 里启用 Office MCP 连接**（连接器列表里有 PowerPoint）
3. **目标 .pptx 文件当前处于打开状态**——MCP 操作的是"前台活动窗口"，文件没开就报错

如果用户没满足条件，**不要硬上**，提示用户：

> 我看你想改 PPTX 文件本身。这需要：① 你的机器装了 PowerPoint；② 已在 Claude 连接器里启用了 Office MCP；③ 目标文件正打开。
> 如果暂时不方便，我可以改用「PPTX 独立生成」（生成一个新的 .pptx 文件不依赖 MCP）或「HTML 单文件」（最快，浏览器看）——选哪个？

## 实现要点

### Step 1 — 背景策略

**复用模板**（用户选了"复用现有模板"）：

```js
// 1. 用 duplicate_slide 复制同主题系列某页
// 2. execute_office_js 列出 shapes
slide.shapes.load("items/id,items/name,items/top,items/left");
await context.sync();
// 3. 保留 id 通常是 8/29/81 等(背景图/标题栏/底栏),删除其余
```

**纯深色背景**（用户选了"纯深色背景"）：

```js
const newSlide = slides.add(SlideLayoutType.titleOnly);
newSlide.background.fill.setSolidFill({color: "#0A0E1A"});
```

### Step 2 — 创建形状骨架

一次 `execute_office_js` 调用，批量 `addTextBox`/`addGeometricShape`，定位置和尺寸。**每个 textBox 必须设置**：

```js
textFrame.autoSizeSetting = "AutoSizeNone";  // 关键!不然字号会被自动收缩
textFrame.wordWrap = true;                   // 金句/注解 true,单行短语 false
textFrame.verticalAlignment = "Top";
textFrame.marginLeft = 0;
textFrame.marginRight = 0;
textFrame.marginTop = 0;
textFrame.marginBottom = 0;
```

### Step 3 — 批量富文本写入

**用单次 `edit_slide_xml` 调用** 遍历所有 shape id，用 `findShapeById` + `replaceTextBody` 一次性写所有 `<a:p>` XML。

为什么不能逐个 `edit_slide_text`：每次调用都会触发 reimport，会闪屏，慢且体验差。

```xml
<a:p>
  <a:r>
    <a:rPr lang="zh-CN" sz="4800" b="1">
      <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
      <a:latin typeface="+mj-lt"/>
      <a:ea typeface="+mj-ea"/>
    </a:rPr>
    <a:t>让方案</a:t>
  </a:r>
  <a:r>
    <a:rPr lang="zh-CN" sz="4800" b="1">
      <a:solidFill><a:srgbClr val="E0762D"/></a:solidFill>
    </a:rPr>
    <a:t>穿透</a:t>
  </a:r>
  <a:r>
    <a:rPr lang="zh-CN" sz="4800" b="1">
      <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
    </a:rPr>
    <a:t>到工序</a:t>
  </a:r>
</a:p>
```

注意：
- `<a:t>` 内的 `&` 必须 escape 成 `&amp;`，用 `escapeXml()` 全局函数
- 字号单位是 1/100 pt（48pt → `sz="4800"`）
- 字体用 `+mj-lt`/`+mj-ea` 继承主题字体

### Step 4 — autosize 必填

`edit_slide_xml` 调用**必须传** `autosize_shape_ids` 数组，列出所有改了文字的形状 id。否则字号溢出框时不会自动调整。

## 验证清单

调用一次 `verify_slide_visual`，检查：

- [ ] 巨幅金句未被截断（超出 960×540 边界）
- [ ] 留白未被压缩（苹果式上下 ≥ 60pt）
- [ ] 底栏 slogan 未被裁切（`y + height > 540` 是常见问题）
- [ ] 数据墙的数字是页面最显眼元素（如果不是，说明字号没起来）

发现问题时**修原元素位置/字号**，不要删了重建——重建会丢掉之前的对齐和富文本设置。

## Done 判断

`verify_slide_visual` 返回 no significant issues，且用户在新页面上明确说"满意/可以/OK"。
