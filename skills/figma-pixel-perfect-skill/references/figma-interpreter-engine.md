# Figma 解释引擎规范

## 概述

Figma 解释引擎是本技能的核心差异化能力。它对 TalkToFigma MCP 采集的原始设计数据进行预处理和语义理解，将充满噪音的 Figma JSON 数据转换为 AI 能准确理解的"干净设计语义"。

## 为什么需要解释引擎

Figma 设计文件中普遍存在以下"非理想"数据：

| 问题类型 | 示例 | 影响 |
|---|---|---|
| 不可见图层 | 透明度 0%、隐藏、被遮挡的元素 | 生成冗余 DOM 节点 |
| 错误分组 | 设计师随意创建的分组框 | 生成无意义的嵌套 div |
| 重叠节点 | 用于对齐的辅助矩形 | 生成多余的定位元素 |
| 意外填充/阴影 | 调试时临时添加的样式 | 样式还原不准确 |
| 空白文本节点 | 占位用的空文本 | 生成空 span 元素 |
| 冗余约束 | 相互矛盾的布局约束 | 布局计算错误 |

通用 LLM 无法有效处理这些噪音，需要专门的预处理层。

## 处理流程

### Step 1: 噪音过滤

对 `read_my_design` 返回的节点树进行递归过滤：

```
过滤规则（按优先级排序）：
1. 移除 opacity === 0 的节点（完全透明）
2. 移除 visibility === "hidden" 的节点
3. 移除 width === 0 || height === 0 的节点（零尺寸）
4. 移除纯空白文本节点（text.trim() === ""）
5. 移除没有填充、描边、子节点的空 Frame（纯辅助框）
6. 标记被完全遮挡的节点（bounds 完全在父节点可见区域外）
```

**TalkToFigma 工具调用：**
- `get_node_info` — 获取单个节点的详细属性，检查 opacity/visibility
- `scan_nodes_by_types` — 批量筛选特定类型节点

### Step 2: 结构修正

分析节点层级关系，修正不合理的分组：

```
修正规则：
1. 单子节点 Frame → 展平（移除多余包装层）
2. 仅用于 Auto Layout 的辅助 Frame → 保留但标记为布局容器
3. 多层嵌套的同类型容器 → 合并为单层
4. 绝对定位的子元素 → 检查是否应转为 Flex/Grid
5. 命名含 "Group" 但无实际功能的分组 → 展平
```

**TalkToFigma 工具调用：**
- `get_nodes_info` — 批量获取节点详情，分析父子关系
- `get_document_info` — 获取页面层级结构

### Step 3: 布局推断

将 Figma 的 Auto Layout 语义转换为 Web 布局语义：

| Figma Auto Layout | Web 布局 | 判断依据 |
|---|---|---|
| layoutMode: HORIZONTAL | `display: flex; flex-direction: row` | 主轴方向 |
| layoutMode: VERTICAL | `display: flex; flex-direction: column` | 主轴方向 |
| primaryAxisAlignItems: CENTER | `justify-content: center` | 主轴对齐 |
| counterAxisAlignItems: CENTER | `align-items: center` | 交叉轴对齐 |
| layoutSizing: HUG | `width: fit-content` | 尺寸模式 |
| layoutSizing: FILL | `width: 100%` | 尺寸模式 |
| itemSpacing: N | `gap: Npx` | 子元素间距 |
| paddingTop/Right/Bottom/Left | `padding: T R B L` | 内边距 |
| layoutWrap: WRAP | `flex-wrap: wrap` | 换行 |

**对于非 Auto Layout 的节点：**
- 检查子元素是否呈网格排列 → 使用 CSS Grid
- 检查子元素是否水平/垂直排列 → 推断为 Flex
- 检查子元素是否使用绝对定位 → 使用 `position: absolute`

### Step 4: 组件识别

识别设计中的可复用 UI 模式：

```
识别策略：
1. 精确匹配：节点类型为 COMPONENT 或 COMPONENT_SET
2. 模式匹配：结构相似的节点组（如多个卡片、列表项）
3. 语义匹配：命名含 "Button"、"Card"、"Input"、"Modal" 等关键词
4. 样式匹配：具有相同样式集合的节点组
```

**TalkToFigma 工具调用：**
- `get_local_components` — 获取所有本地组件定义
- `scan_nodes_by_types` — 扫描 COMPONENT/COMPONENT_SET 类型节点

### Step 5: 层级规范化

统一节点层级，消除冗余嵌套：

```
规范化规则：
1. 每个 Figma Frame → 对应一个 DOM 容器（div/section/article）
2. 每个 Figma Component → 对应一个 React/Vue 组件
3. 每个 Figma Text → 对应一个语义化文本元素（h1-h6/p/span/label）
4. 每个 Figma Rectangle（有填充）→ 对应一个 div 或语义化元素
5. 每个 Figma Rectangle（无填充）→ 检查是否为分隔线/装饰元素
6. 每个 Figma Image → 对应一个 img 元素
```

## 输出格式

解释引擎处理完成后，输出结构化的设计语义数据：

```json
{
  "componentTree": [
    {
      "id": "node-id",
      "name": "Header",
      "type": "COMPONENT",
      "semanticRole": "header",
      "layout": {
        "display": "flex",
        "flexDirection": "row",
        "alignItems": "center",
        "justifyContent": "space-between",
        "padding": "16px 24px",
        "gap": "12px"
      },
      "tokens": {
        "backgroundColor": "#FFFFFF",
        "borderBottom": "1px solid #E5E7EB"
      },
      "children": [...]
    }
  ],
  "designTokens": {
    "colors": {...},
    "typography": {...},
    "spacing": {...},
    "borders": {...},
    "shadows": {...}
  },
  "reusableComponents": ["Header", "Button", "Card", "Input"],
  "assets": [
    {"type": "image", "nodeId": "...", "exportFormat": "PNG"},
    {"type": "svg", "nodeId": "...", "exportFormat": "SVG"}
  ]
}
```

## 注意事项

1. **不要跳过解释引擎**：直接将原始 Figma 数据丢给 LLM 会导致大量噪音和错误
2. **保留设计意图**：过滤噪音时不要误删有效节点，保守处理
3. **尊重 Auto Layout**：Figma 的 Auto Layout 是设计师明确表达的布局意图，优先信任
4. **组件边界清晰**：每个组件应有明确的输入（Props）和输出（渲染结果）
5. **资产引用完整**：所有图片、SVG、图标必须正确导出和引用
