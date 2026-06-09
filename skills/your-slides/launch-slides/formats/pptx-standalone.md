# 输出格式 — PPTX 独立生成（pptx 技能，不依赖 MCP）

通过调用 `anthropic-skills:pptx` 技能离线生成一个 .pptx 文件。**用户机器不需要安装 PowerPoint，也不需要任何 MCP 连接器**。

## 适用场景

- 用户想要 .pptx 文件本身（发邮件、上传到云盘、归档）
- 用户机器是 Linux / iPad / 没装 Office / 没连 Office MCP
- 不需要在用户当前打开的 PPT 里就地修改

## ⚠️ 关键限制条件（必须告知用户）

1. **生成的是新文件**，不是修改用户已有的 .pptx——不能"在原文件第 5 页插入一页"，只能"生成一个新 .pptx 文件，里面是改造后的发布会页"
2. **没有模板继承**：用户原文件的标题栏/底栏/背景图无法保留，每页是从空白开始画
3. **富文本精度比 Office MCP 路径低**：金句关键词换色可以做，但 PPT 主题字体继承、复杂段落格式都更弱
4. **使用前必须调用 pptx 技能**：`Read` `/var/folders/.../skills/pptx/SKILL.md` 来获取最新的工具链说明

## 实现要点

### Step 0 — 先调用 pptx 技能

```
Read /var/folders/.../skills/pptx/pptxgenjs.md
```

让 pptx 技能告诉你当前的最佳生成方式（pptxgenjs / python-pptx / unpacking 等）。**不要凭记忆**，pptx 工具链经常更新。

### Step 1 — 颜色和尺寸约定

按 `styles/*.md` 的配色和坐标，但要注意：

- pptxgenjs 的坐标单位是 inch（1 inch ≈ 72pt）
- 960×540 pt = 13.33 × 7.5 inch
- 颜色去掉 `#` 前缀：`#E0762D` → `"E0762D"`
- 字号直接用 pt 数字

### Step 2 — 用 pptxgenjs 写一页发布会风格的最小示例

```js
const PptxGenJS = require("pptxgenjs");
const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE";  // 16:9, 13.33×7.5 inch

const slide = pres.addSlide();
slide.background = {color: "0A0E1A"};

// 顶部 tag
slide.addText("产品价值 · PRODUCT VALUE", {
  x: 0.67, y: 0.33, w: 6, h: 0.3,
  fontSize: 14, color: "E0762D", bold: false, charSpacing: 2
});

// 巨幅金句(关键词换色用富文本数组)
slide.addText([
  {text: "让方案", options: {color: "FFFFFF"}},
  {text: "穿透", options: {color: "E0762D"}},
  {text: "到工序", options: {color: "FFFFFF"}}
], {
  x: 0.67, y: 1.6, w: 12, h: 1.2,
  fontSize: 48, bold: true, fontFace: "PingFang SC"
});

// 4 个价值点(每列三个 textbox)
const items = [
  ["01", "穿透工序", "方案触发二次交底,每个工序都有依据"],
  ["02", "拦截偏差", "传统归档→自动拦截,延期 ↓14 天"],
  ["03", "数据沉淀", "每个项目沉淀数据,服务下一个"],
  ["04", "决策闭环", "管理层看板,从 0→1 重塑流程"]
];
items.forEach((item, i) => {
  const x = 0.67 + i * 3.1;
  slide.addText(item[0], {x, y: 5.0, w: 2.5, h: 0.4, fontSize: 28, color: "E0762D"});
  slide.addText(item[1], {x, y: 5.4, w: 2.5, h: 0.3, fontSize: 20, color: "FFFFFF", bold: true});
  slide.addText(item[2], {x, y: 5.9, w: 2.5, h: 0.6, fontSize: 12, color: "9CB3CC"});
});

await pres.writeFile({fileName: "launch-slide.pptx"});
```

### Step 3 — 在多页序列模式下

每个 `pres.addSlide()` 生成一页。按 Step 2 风格选择给的页序列（开场金句/痛点/转折/特性/对比/数据/价值/CTA）逐页 add。

### Step 4 — 输出文件位置

写入用户的工作目录（默认 outputs/ 或用户指定的文件夹），文件名用金句关键词，例如 `launch-穿透工序.pptx`。

## 验证清单

- [ ] 文件能用 PowerPoint / Keynote / WPS 正常打开
- [ ] 16:9 比例（如果 wrong layout，整页会变形）
- [ ] 巨幅金句字号正确（pt 而不是 pptxgenjs 默认值）
- [ ] 关键词换色生效
- [ ] 中文字体没有变成系统默认衬线（指定 fontFace 是关键）

## 用户拿到文件后能做什么

- 双击用 PowerPoint / Keynote / WPS 打开
- 可以在 PPT 里继续编辑——但建议用户先复制一份再改
- 如果想合并到已有 PPT：用 PPT 的"重用幻灯片"功能，或者手动复制粘贴页面

不要承诺 pptxgenjs 生成的文件能"完美继承用户原 PPT 的母版"——做不到。
