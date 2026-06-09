# Figma 像素级还原技能 — 安装指南

## 技能文件结构

```
figma-pixel-perfect/
├── SKILL.md                                    # 核心技能定义
├── agents/
│   └── openai.yaml                             # UI 配置 + MCP 依赖声明
├── assets/
│   ├── icon-small.svg                          # 小图标
│   └── icon-large.svg                          # 大图标
└── references/
    ├── figma-interpreter-engine.md             # Figma 解释引擎规范
    ├── design-token-extraction.md              # 设计 Token 提取规范
    ├── browser-verification-engine.md          # 浏览器验证引擎规范
    └── code-generation-rules.md                # 代码生成规则
```

## 安装到 SOLO

将 `figma-pixel-perfect/` 文件夹复制到 SOLO 的技能目录：

```bash
cp -r figma-pixel-perfect/ ~/.solo/skills/figma-pixel-perfect/
```

或通过 SOLO 的技能管理界面导入。

## 安装到 Trae

将 `figma-pixel-perfect/` 文件夹复制到 Trae 的技能目录：

```bash
cp -r figma-pixel-perfect/ ~/.trae/skills/figma-pixel-perfect/
```

## 前置 MCP 依赖

本技能依赖以下 MCP Server，需提前配置：

### 1. TalkToFigma MCP Server

在 SOLO/Trae 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "TalkToFigma": {
      "command": "npx",
      "args": ["-y", "cursor-talk-to-figma-mcp@latest"]
    }
  }
}
```

### 2. integrated_browser（SOLO 内置）

SOLO 默认已配置，无需额外操作。

## 使用方式

安装完成后，在 SOLO/Trae 中：

1. 确保 Figma 桌面端已打开，TalkToFigma 插件已运行
2. 在 Figma 中选中目标设计节点
3. 发送指令：
   ```
   Use Skill: figma-pixel-perfect，将当前 Figma 选区转换为 React + Tailwind 代码
   ```
