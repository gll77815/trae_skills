# Gap Analysis 方法论

> 本文档是 `figma-pixel-perfect` 技能 Phase 5 的详细参考。
> Gap Analysis 是连接"理解现有代码"与"生成新代码"的关键桥梁。

## 核心原则

**"Validate, Don't Rebuild"** — 已有的、可复用的代码和 Token 只验证不重建。只对真正缺失或差异明显的部分进行新建或修改。

## Gap Analysis 的三个层次

Gap Analysis 在三个维度上执行：

```
┌─────────────────────────────────────────────┐
│           Gap Analysis 三层模型              │
├─────────────────────────────────────────────┤
│                                             │
│  Layer 1: 组件级 Gap Analysis                │
│  → 对比 Figma 组件 vs 现有代码组件           │
│  → 输出: ✅/⚠️/❌ 状态标记                   │
│                                             │
│  Layer 2: 资产级 Gap Analysis                │
│  → 对比 Figma 资产 vs 现有静态资源           │
│  → 输出: 复用/导出/替换 决策                 │
│                                             │
│  Layer 3: Token 级 Gap Analysis              │
│  → 对比 Figma Token vs 现有设计 Token        │
│  → 输出: Match/Close/Mismatch/New 状态       │
│                                             │
└─────────────────────────────────────────────┘
```

## Layer 1: 组件级 Gap Analysis

### 分析流程

```
Figma 设计组件列表（来自 Phase 2）
        ↓
现有组件清单（来自 Phase 1.3）
        ↓
逐一对比 → 生成状态标记
        ↓
输出 Gap Analysis 表格
```

### 状态定义

| 状态 | 标记 | 含义 | 处理策略 |
|---|---|---|---|
| Complete | ✅ | 现有组件与 Figma 设计基本一致 | **仅验证**，不修改代码 |
| Audit Needed | ⚠️ | 现有组件存在但与设计有差异 | **修改**现有组件 |
| Missing | ❌ | 现有代码中不存在对应组件 | **新建**组件 |

### 判断规则

**标记为 ✅ Complete 的条件（需全部满足）：**
1. 组件功能与 Figma 设计一致
2. 视觉样式（颜色/字体/间距/圆角）偏差在容差范围内
3. 组件 Props 接口满足设计需求
4. 响应式行为与设计一致

**标记为 ⚠️ Audit Needed 的条件（满足任一）：**
1. 组件功能基本一致，但样式有偏差
2. 缺少 Figma 设计中的某些子元素
3. 布局方式不同（如 Figma 是 Flex，代码是 Grid）
4. 交互行为不完整（缺少 hover/focus 等状态）

**标记为 ❌ Missing 的条件：**
1. 现有代码中不存在功能相似的组件
2. 现有组件的功能差异过大，修改成本超过新建

### 对比维度

对每个组件，从以下维度进行对比：

| 维度 | 对比内容 | 权重 |
|---|---|---|
| 功能 | 组件是否实现了设计中的功能 | 高 |
| 结构 | DOM/组件结构是否与设计层级一致 | 中 |
| 样式 | 颜色/字体/间距/圆角/阴影是否一致 | 高 |
| 布局 | Flex/Grid 方向、对齐、间距是否一致 | 高 |
| 交互 | hover/active/focus/disabled 状态是否完整 | 中 |
| 响应式 | 断点行为是否与设计一致 | 低 |
| 可访问性 | aria 属性、键盘导航是否完整 | 低 |

### 输出格式

```
| # | Section/组件 | Figma 设计描述 | 现有代码 | 状态 | 关键差距 | 处理策略 | 优先级 |
|---|---|---|---|---|---|---|---|
| 1 | Header | 固定顶部, 80px高 | Header.tsx | ⚠️ | 高度不匹配 | 修改 | P1 |
| 2 | Sidebar | 350px宽, 可折叠 | Sidebar.tsx | ⚠️ | 缺折叠功能 | 修改 | P1 |
| 3 | StatsCard | 4列网格, 数据展示 | 无 | ❌ | 完全缺失 | 新建 | P1 |
| 4 | DataTable | 排序+分页 | DataTable.tsx | ✅ | - | 验证 | P2 |
```

## Layer 2: 资产级 Gap Analysis

### 分析流程

```
Figma 资产清单（来自 Phase 2.7）
        ↓
现有静态资源扫描（Glob: src/assets/**, public/**）
        ↓
逐一对比 → 生成复用/导出/替换决策
        ↓
输出资产 Gap 表格
```

### 资产匹配规则

| 状态 | 标记 | 条件 | 处理方式 |
|---|---|---|---|
| Match | ✅ | 文件存在且内容与设计一致 | 直接复用 |
| Different | ⚠️ | 文件存在但内容与设计不同 | 替换为新版本 |
| Missing | ❌ | 文件不存在 | 从 Figma 导出 |
| CSS Implementable | 💡 | 可用 CSS 实现（渐变/纯色块） | 不导出，用 CSS 实现 |

### 资产分类

| 资产类型 | 导出格式 | 存放路径 |
|---|---|---|
| Logo / 品牌图标 | SVG | `src/assets/icons/` |
| 功能图标（搜索/菜单/设置等） | SVG | `src/assets/icons/` |
| 照片 / 插画 | PNG / WebP | `src/assets/images/` |
| 背景图案 | SVG / CSS | `src/assets/images/` 或 CSS 实现 |
| 纯色块 / 渐变 | CSS | 不导出，用 CSS 实现 |

### 输出格式

```
| # | 资产名称 | Figma 类型 | 尺寸 | 项目现有 | 状态 | 处理方式 | 目标路径 |
|---|---|---|---|---|---|---|---|
| 1 | logo-main | SVG | 120×32 | ✅ | ✅ Match | 复用 | src/assets/icons/logo.svg |
| 2 | icon-search | SVG | 20×20 | ❌ | ❌ Missing | 导出 | src/assets/icons/search.svg |
| 3 | hero-bg | 渐变 | 1920×600 | ❌ | 💡 CSS | CSS实现 | - |
```

## Layer 3: Token 级 Gap Analysis

### 分析流程

```
Figma 提取的 Token（来自 Phase 4.1）
        ↓
现有项目 Token（来自 Phase 1.4）
        ↓
逐一对比 → 生成匹配状态
        ↓
汇总 Token 差异报告
```

### Token 匹配规则

| 状态 | 标记 | 条件 | 处理策略 |
|---|---|---|---|
| Match | ✅ | 值完全一致（精确匹配） | 直接复用，不创建新的 |
| Close | ⚠️ | 值接近（颜色 ΔE < 3，尺寸偏差 ≤ 1px） | 使用现有 Token，记录偏差 |
| Mismatch | ❌ | 值差异明显 | 创建新 Token 或更新现有 Token |
| New | ➕ | Figma 有但项目缺失 | 创建新 Token |
| Unused | ➖ | 项目有但 Figma 未使用 | 标记，不删除 |

### Token 对比方法

**颜色对比：**
- 将 Figma 颜色值（RGBA）转换为 HEX
- 与项目 Token 中的 HEX 值对比
- 计算 ΔE（CIE76 公式），ΔE < 3 视为 Close

**尺寸对比：**
- 直接比较 px 值
- 偏差 ≤ 1px 视为 Close

**字体对比：**
- font-family: 字符串完全匹配
- font-size: 偏差 ≤ 1px 视为 Close
- font-weight: 数值完全匹配

### 输出格式

```
| Token 类别 | Token 名称 | Figma 值 | 项目现有值 | 状态 | 处理策略 |
|---|---|---|---|---|---|
| 颜色 | primary | #3B82F6 | #3B82F6 | ✅ Match | 复用 |
| 颜色 | background | #F8FAFC | #F9FAFB | ⚠️ Close | 复用（ΔE=0.8） |
| 颜色 | accent | #8B5CF6 | - | ➕ New | 创建 |
| 间距 | card-padding | 20px | 16px | ❌ Mismatch | 新建 |
```

## 汇总报告

完成三层分析后，输出汇总报告：

```
## Gap Analysis 汇总报告

### 组件级统计
| 状态 | 数量 | 占比 | 工作量 |
|---|---|---|---|
| ✅ Complete | 3 | 30% | 验证 |
| ⚠️ Audit Needed | 4 | 40% | 修改 |
| ❌ Missing | 3 | 30% | 新建 |

### 资产级统计
| 状态 | 数量 | 工作量 |
|---|---|---|
| ✅ Match | 8 | 无 |
| ⚠️ Different | 3 | 替换 |
| ❌ Missing | 5 | 导出 |
| 💡 CSS | 4 | CSS 实现 |

### Token 级统计
| 状态 | 数量 | 工作量 |
|---|---|---|
| ✅ Match | 12 | 无 |
| ⚠️ Close | 5 | 记录偏差 |
| ❌ Mismatch | 3 | 新建/更新 |
| ➕ New | 7 | 创建 |

### 总体工作量估算
- 新建组件: 3 个
- 修改组件: 4 个
- 验证组件: 3 个
- 新建 Token: 10 个
- 导出/替换资产: 8 个
- 预估总工时: ~8h
```

## 常见问题处理

### Q: 如何判断"修改"还是"新建"？
- 如果现有组件的功能与设计目标一致，但样式/结构有差异 → **修改**
- 如果现有组件的功能与设计目标不同，或修改成本超过新建 → **新建**
- 经验法则：修改超过 50% 的代码时，考虑新建

### Q: Token 差异很小（如 #F8FAFC vs #F9FAFB），怎么处理？
- 如果 ΔE < 3（人眼几乎不可感知），标记为 ⚠️ Close，使用现有值
- 在报告中记录偏差，供设计团队审查

### Q: Figma 中的组件与现有组件功能相似但不完全一致？
- 标记为 ⚠️ Audit Needed
- 在"关键差距"列中详细说明差异
- 由用户决定是修改现有组件还是新建

### Q: 如何处理 Figma 中的设计系统组件（如 Ant Design 组件）？
- 检查项目是否已安装对应的组件库
- 如果已安装，标记为 ✅ Complete，验证版本和样式
- 如果未安装，标记为 ❌ Missing，建议安装组件库而非手写
