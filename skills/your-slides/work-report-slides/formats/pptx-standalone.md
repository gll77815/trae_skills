# 输出格式 — PPTX 独立生成（pptx 技能，不依赖 MCP）

通过 `anthropic-skills:pptx` 离线生成新的 .pptx 文件。**最适合工作汇报场景的"发邮件归档"**——周会后导出附件，或月底归档项目复盘。

## 适用场景

- 用户要把汇报作为邮件附件发出去
- 用户机器没装 PowerPoint 或没启用 Office MCP
- 用户要把汇报归档到 SharePoint / 飞书云盘
- 不需要在用户当前打开的 PPT 里直接编辑

## ⚠️ 关键限制条件（必须告知用户）

1. **生成的是新文件**，不修改用户现有的 .pptx
2. **没有公司模板继承**：用户原有 PPT 的页眉/页脚/水印无法保留——这点工作汇报场景**特别敏感**，很多公司要求所有外发文件必须用统一模板。如果用户公司有严格模板要求，**建议改用 Office MCP 路径**
3. **富文本/动画精度低**：状态灯、表格、timeline 能做，但复杂动画（如时间线渐入）做不了
4. **使用前必须调用 pptx 技能**：`Read /var/folders/.../skills/pptx/SKILL.md` 获取最新工具链

## 实现要点

### Step 0 — 先调用 pptx 技能

```
Read /var/folders/.../skills/pptx/pptxgenjs.md
```

**不要凭记忆**，pptx 工具链经常更新。

### Step 1 — 颜色和尺寸约定

- pptxgenjs 坐标单位是 inch（1 inch ≈ 72pt）
- 960×540 pt = 13.33 × 7.5 inch
- 颜色去掉 `#`：`#22C55E` → `"22C55E"`

### Step 2 — 一个周报页的最小示例

```js
const PptxGenJS = require("pptxgenjs");
const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE";

const slide = pres.addSlide();
slide.background = {color: "FFFFFF"};

// 主标题 + 总状态灯
slide.addText("2026 W18 周报 · 产品工程组", {
  x: 0.33, y: 0.33, w: 8, h: 0.5,
  fontSize: 28, color: "1F2937", bold: true,
  fontFace: "PingFang SC"
});

// 总状态灯（用 ellipse shape）
slide.addShape(pres.ShapeType.ellipse, {
  x: 10.5, y: 0.5, w: 0.18, h: 0.18, fill: {color: "22C55E"}, line: {type: "none"}
});
slide.addText("整体绿灯", {
  x: 10.8, y: 0.42, w: 2, h: 0.4, fontSize: 16, color: "1F2937"
});

// 三栏：上周完成 / 本周计划 / 风险
const COL_WIDTH = 4.1;
const COL_X = [0.33, 4.66, 8.99];
["✓ 上周完成", "▶ 本周计划", "⚠ 风险阻塞"].forEach((title, i) => {
  slide.addText(title, {
    x: COL_X[i], y: 1.4, w: COL_WIDTH, h: 0.4,
    fontSize: 18, color: "1F2937", bold: true
  });
});

// 风险栏的状态灯 + 文字
slide.addShape(pres.ShapeType.ellipse, {
  x: 9.0, y: 1.95, w: 0.14, h: 0.14, fill: {color: "F59E0B"}, line: {type: "none"}
});
slide.addText("A 上线后埋点数据缺失", {
  x: 9.22, y: 1.85, w: 4, h: 0.35, fontSize: 12, color: "1F2937"
});

// 底部 KPI 行
slide.addText("关键指标: DAU 1.2M ↑3% · 转化 2.4% 🟡 · 故障 1 🔴", {
  x: 0.33, y: 6.8, w: 13, h: 0.4, fontSize: 14, color: "1F2937"
});

await pres.writeFile({fileName: "2026-W18-周报.pptx"});
```

### Step 3 — 表格（月度复盘风格）

pptxgenjs 表格用 `slide.addTable(rows, options)`，传二维数组：

```js
const tableData = [
  // 表头
  [
    {text: "指标", options: {bold: true, fill: "F1F5F9"}},
    {text: "目标", options: {bold: true, fill: "F1F5F9"}},
    {text: "实际", options: {bold: true, fill: "F1F5F9"}},
    {text: "状态", options: {bold: true, fill: "F1F5F9"}},
    {text: "偏差归因", options: {bold: true, fill: "F1F5F9"}}
  ],
  // 数据行
  ["DAU", "1.2M", "1.25M", "🟢", "-"],
  ["付费转化", "3.0%", "2.4%", "🟡", "新渠道质量低,已切换"],
  ["重大事故", "0", "1", "🔴", "A 项目迁移失败,已回滚"]
];

slide.addTable(tableData, {
  x: 0.33, y: 2.5, w: 12.66,
  fontSize: 13, fontFace: "PingFang SC",
  border: {pt: 0.5, color: "E5E7EB"},
  rowH: 0.42
});
```

⚠️ pptxgenjs 表格的状态灯如果用 emoji（🟢🟡🔴），在不同 Office 版本上颜色可能漂移。**更稳的做法**：状态列留空，单独 `addShape(ellipse)` 在表格对应位置画圆点。但实现复杂，需要精确计算坐标。

### Step 4 — Timeline（项目里程碑风格）

pptxgenjs 没有直接的 timeline 组件，要用基础形状组合：

```js
// 主线
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 2.55, w: 12.2, h: 0.03, fill: {color: "E5E7EB"}, line: {type: "none"}
});
// 节点（5 个等分）
const nodes = [
  {x: 0.5, color: "22C55E"},   // 已完成
  {x: 3.55, color: "22C55E"},
  {x: 6.6, color: "F59E0B"},   // 进行中
  {x: 9.65, color: "CBD5E1"},  // 未来
  {x: 12.7, color: "CBD5E1"}
];
nodes.forEach(n => {
  slide.addShape(pres.ShapeType.ellipse, {
    x: n.x - 0.1, y: 2.45, w: 0.2, h: 0.2, fill: {color: n.color}, line: {type: "none"}
  });
});
```

### Step 5 — 多页时

每页一个 `pres.addSlide()`。按 Step 2 Q4 选的页序列（封面/BLUF/KPI/完成/计划/风险/行动/附录）逐页 add。

### Step 6 — 输出文件位置

文件名约定：
- 周报：`2026-W18-周报.pptx`
- 月报：`2026-05-月度复盘.pptx`
- 项目：`A项目-W18-里程碑汇报.pptx`
- 向上：`向CEO-2026-W18-汇报.pptx`

## 验证清单

- [ ] 用 PowerPoint / Keynote / WPS 都能打开
- [ ] 16:9 比例正确
- [ ] 中文字体没变成系统衬线（指定 fontFace="PingFang SC" 等）
- [ ] 状态灯颜色与全局规范一致
- [ ] 表格行高足够、不挤
- [ ] 数字单位（K/M/万）全页一致

## 用户拿到文件后

- 双击用 PowerPoint / Keynote / WPS 打开
- 发邮件直接附件，是工作汇报最常见用法
- 想合并到公司模板里：用 PPT 的"重用幻灯片"功能，或手动复制粘贴
- 想加公司 logo：在 PPT 里手动加，或回头用 Office MCP 路径直接做

**不要承诺**：完美继承用户原 PPT 的公司模板/水印/页眉页脚——做不到。
