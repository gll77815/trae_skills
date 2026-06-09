# Agent-Alias：“翠花，上酸菜！” - 给你的skills起个中文名

## 1、Skill 简介

**Agent Alias（智能体命名与编排）** 是一个帮助你用"角色化"方式创建和管理 AI 智能体(或者skills)的 Skill。

简单来说：
- 你可以给你的股票Skill命名“马斯克”或者“老贾”，which means 喊他就可以帮你搞钱了
- 另外设岗位、配能力、划边界，然后像叫同事一样，通过 `/姓名` 直接唤醒

适合所有安装了大量 Skills/Agents 但苦于"找不到、记不住、不会组合"的用户。

## 2、使用场景

### 我的痛点

随着 SOLO 上可用的 Skill 越来越多，我遇到了一个很现实的问题：

**技能列表越来越长，全是英文名，根本记不住哪个是干嘛的。**

每次想用某个 Skill，都要在列表里翻半天，好不容易找到了，还得回忆它的触发词是什么。更头疼的是，有些复杂任务需要组合多个 Skill，但我经常搞混它们的用途和边界。

![image|690x384](upload://wFLFqGv4AXVeZj6Wsjt5cFdhquc.jpeg)


### 灵感来源

有一天我在想：为什么不能像“喊妈”一样唤醒 AI 技能呢？

在真实的工作中，我们不会对着职位叫人“那个角落的PM过来帮我搞个事情”（除非你真的不认识他，而且也太不礼貌）——正常人叫的是"翠花"、"老马"、“达叔”（我的老搭档）。从一个名字，我就能立刻反应过来他是做什么的、擅长什么、边界在哪里。

**如果 AI 技能也能这样管理呢？**

这就是 Agent Alias 的诞生初衷。

### 解决了什么

| 之前                | 之后                |
| ----------------- | ----------------- |
| 在技能列表里翻找英文 Skill  | 输入 `/达叔` 直接唤醒     |
| 记不住 Skill 的触发词和用途 | 看到名字就知道能力         |
| 不知道哪些 Skill 能组合用  | 一个智能体自动编排多个 Skill |
| 每次都要手动写长串 Prompt  | 智能体自带角色设定和边界约束    |


![image|690x384](upload://xgQnkCFuExONPWJohjpckrwDLsZ.jpeg)


## 3、创作过程

### 第一步：需求梳理与头脑风暴

先通过头脑风暴明确了核心需求：

- 智能体/skills需要有**姓名、岗位、能力标签、工作边界**
- 支持**中文命名 + 拼音调用**（`/达叔` 或 `/dashu` - 这里用拼音主要解决斜杠命令无法用中文唤醒的问题，如果没有这个癖好直接中文喊也能唤醒Skill）
- 创建后能**直接斜杠唤醒**，不需要额外配置

![image|690x433](upload://rh9RQ1e0KSJbZ7mBQJuu0qD32Qo.jpeg)
![image|690x433](upload://qzuQ9cHtA21xSAXPYzSyDbN52sC.png)


### 第二步：架构设计

经过多轮讨论，确定了关键设计决策：

- **存储方式**：每个智能体生成独立的 `SKILL.md`，存放在 `.trae/skills/` 下，作为子技能被系统直接识别
- **防循环依赖**：智能体只能调用基础 Skill，不能调用其他智能体
- **删除保护**：删除智能体时自动检查工作组引用，提示影响范围

![image|690x433](upload://4ylsVglhKMzrOLC4W1fDO2h8H11.jpeg)


### 第三步：Skill 文件编写

最终产出了以下文件结构：

```
agent-alias/
├── SKILL.md                    # 主技能（路由调度 + 管理逻辑）
├── README.md                    # 使用说明
└── workflows/                   # 管理流程文档
    ├── create-agent.md          # 创建智能体
    ├── create-workgroup.md      # 创建工作组
    ├── query-search.md          # 查询检索
    └── update-delete.md         # 更新删除
```

### 第四步：实测验证

用"达叔"这个产品经理角色做了完整的创建-唤醒-更新-删除测试：

1. 创建达叔 → 自动生成子技能 SKILL.md
2. `/dashu 帮我设计登录流程` → 成功唤醒并以产品经理身份工作
3. 给达叔添加 `slides` 技能 → 更新成功，获得 PPT 编制能力
4. 验证边界约束 → 达叔拒绝写代码 ✅（不要再卷他了）

![image|690x433](upload://yFuEv2C6nET58gg3G1ZAPbVavne.png)
![image|690x433](upload://rYto2DwpBILMXfGojtHiDm7HzRZ.png)
![image|690x433](upload://lR5b9OwX2RjlJ18ZXtZoxdsO9zm.png)


### 第五步：发布前检查

做了完整的发布前审查，修复了 7 个问题：

- 移除私人智能体数据（不随公共 Skill 发布）
- 统一所有文档从 JSON 格式更新为 SKILL.md 格式
- 清除硬编码绝对路径
- 添加 README.md 使用说明

## 4、使用步骤

### 快速上手（3 步）

**第 1 步：安装 Skill**

- 下载 `agent-alias`

> https://github.com/gll77815/trae_skills/tree/main/skills/agent-alias

- 将 `agent-alias` 解压后的文件夹放入 `.trae/skills/` 目录或者直接压缩包导入trae的技能中

**第 2 步：创建/修改你的第一个智能体**

```
示例：
创建智能体达叔，是产品经理，擅长需求设计和业务评审，
核心依赖 bmad-agent-pm 技能，业务讨论时使用 bmad-brainstorming，
不允许直接写代码
```

系统会引导你补充信息，然后自动生成一个可斜杠唤醒的子技能。

**第 3 步：直接唤醒**

```
/达叔 帮我设计一个登录流程
```
![image|690x384](upload://lQp0x7g7gUKRy5xIhsxArwcHs47.jpeg)


### 进阶用法

| 操作 | 指令 |
|------|------|
| 查看所有智能体 | `查询智能体` |
| 按能力搜索 | `找找能做PRD的` |
| 给智能体添加技能 | `给达叔添加 slides 技能` |
| 创建工作组 | `创建工作组产品团队，组长达叔，成员老王` |
| 删除智能体 | `删除智能体达叔` |

## 5、效果展示

### 创建智能体
> ![image|277x500](upload://tg8dpIK9yVEaWn44BBlhiV8UQkP.jpeg)

### 斜杠唤醒

> ![image|690x433](upload://wkmPWjFL3JzCvc8BRACTXcDkERW.png)

### 身份卡片展示

> ![image|690x433](upload://jawNOWBf8Ie8XFaCl6dZYVE7pUo.png)

### 智能体能力扩展

> ![image|345x500](upload://ia6OMWux5ObkfALk0a71Tk131Fa.jpeg)

## 6、Skill 链接

- **Skill 名称**：agent-alias
- **GitHub 地址**：> https://github.com/gll77815/trae_skills/tree/main/skills/agent-alias
- **技能文件**：
```
agent-alias/
├── SKILL.md                    # 主技能（路由调度 + 管理逻辑）
├── README.md                    # 使用说明
└── workflows/                   # 管理流程文档
    ├── create-agent.md          # 创建智能体
    ├── create-workgroup.md      # 创建工作组
    ├── query-search.md          # 查询检索
    └── update-delete.md         # 更新删除
```

## 7、总结与思考

### 最满意的地方

**"像叫同事一样叫 AI"这个隐喻真正落地了。**

创建达叔之后，我不再需要去技能列表里找 `bmad-agent-pm`，也不用记各种触发词。直接说"达叔，帮我设计登录流程"，一切就自然发生了。这种体验和真实工作中叫同事帮忙的感觉非常接近。

### 技术上的收获

1. **子技能架构**：让每个智能体成为独立的 SKILL.md 子技能，既解决了斜杠唤醒问题，又保持了管理上的统一
2. **边界约束设计**：通过"能做/不能做"的显式声明，让 AI 在执行过程中自我约束，避免越界
3. **引用式技能包**：智能体不复制 Skill 内容，而是引用已有 Skill，保持同步更新

### 后续优化方向

- [ ] 增加**智能体模板库**，预设常见角色（产品经理、前端开发、测试工程师等），一键创建
- [ ] 增加**使用统计**，记录每个智能体的调用次数和成功率
- [ ] 支持**导入/导出**，方便团队间分享智能体配置
- [ ] 探索**工作组协商模式**，支持多轮讨论式的协作

### 希望大家怎么体验

建议从创建一个你最熟悉的角色开始——比如你们团队里的产品经理、前端开发、或者测试同学。给它起个名字，配上它真正擅长的 Skill，然后试试用 `/姓名` 唤醒它。

你会发现，当 AI 有了名字和身份之后，交互的感觉完全不一样了。

---

> 欢迎在评论区交流体验感受，也期待看到大家创建的各种有趣智能体！
