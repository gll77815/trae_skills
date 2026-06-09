# B端行业数字化可行性调研 - 快速入门指南

## 5分钟快速上手

### 场景：调研"制造业数字化转型"机会

#### Step 1: 准备调研框架（5分钟）

创建一个Word文档，包含以下8大模块：

```
制造业全景扫描_调研框架.docx
├── 1. 行业概况与发展趋势
├── 2. 政策法规与监管环境
├── 3. 产业链图谱与价值分布
├── 4. 市场主体与竞争格局
├── 5. 技术发展趋势
├── 6. 市场规模与增长预测
├── 7. 数字化转型痛点与机会
└── 8. 切入建议与风险提示
```

#### Step 2: 构建竞品-场景矩阵（10分钟）

使用脚本生成矩阵：

```python
from scripts.generate_matrix import build_matrix
from scripts.generate_excel_matrix import create_excel_matrix

# 定义场景
scenes = [
    {
        "name": "智能质检",
        "type": "生产运营",
        "pain_points": "人工质检效率低、漏检率高",
        "target_customers": "制造型企业",
        "qualification": "无",
        "feasibility": "",
        "market_shares": {"阿里云": "极高(70-80%)", "华为": "中(30-40%)"}
    },
    # ... 更多场景
]

# 定义竞品
competitors = [
    {"name": "阿里云", "category": "互联网系"},
    {"name": "华为", "category": "行业龙头系"},
    {"name": "用友", "category": "第三方专业厂商"},
]

# 生成Word矩阵
build_matrix("制造业", scenes, competitors, "制造业_竞品场景矩阵.docx")

# 生成Excel矩阵
create_excel_matrix("制造业", scenes, competitors, "制造业_竞品场景矩阵.xlsx")
```

#### Step 3: 标注可切入场景（5分钟）

在Excel矩阵的"场景可行性"列标注：
- **可切入**：有市场空间且团队有能力切入
- **PASS**：竞品太强或市场太小
- **观望**：政策不确定或技术不成熟

#### Step 4: 深度调研重点场景（每场景30分钟）

对标注为"可切入"的场景，生成深度调研文档：

```
01_智能质检_深度调研与售前方案.docx
├── 1. 场景概述与政策背景
├── 2. 市场规模与增长趋势
├── 3. 目标客户画像
├── 4. 业务流程与架构设计
├── 5. 竞品分析
├── 6. 商业模式与定价策略
├── 7. 实施路径与里程碑
├── 8. 风险与挑战
└── 9. 售前解决方案摘要
```

#### Step 5: ROI分析（10分钟）

```python
from scripts.roi_summary import create_roi_summary_excel

# 准备ROI数据
scenes_roi = [
    {
        "scene_name": "智能质检",
        "customer_investment": "80万元",
        "annual_benefit": "节省人工成本120万元/年",
        "payback_period": "8个月",
        "five_year_roi": "650%",
    },
    # ... 更多场景
]

# 生成ROI汇总Excel
create_roi_summary_excel(scenes_roi, "制造业", "制造业_ROI汇总.xlsx")
```

输出结果：
- 按ROI评级排序（★★★★★ 强推 → ★☆☆☆☆ 观望）
- 4梯队推荐（强推/推荐/可选/观望）

#### Step 6: 路径规划（10分钟）

基于ROI分析结果，制定切入路径：

```
Phase 1 快赢期（0-6个月）
├── 选择：智能质检（★★★★★）
├── 原因：研发投入低、回收快、团队基因匹配
└── 目标：快速验证市场，获取首批客户

Phase 2 平台期（6-12个月）
├── 建设：AI视觉平台
├── 复用：扩展至智能巡检、安全监控等场景
└── 目标：降低边际研发成本

Phase 3 深水期（12-24个月）
├── 选择：设备预测性维护（★★★☆☆）
├── 原因：高利润但需要补齐行业Know-How
└── 目标：提升客单价和利润率
```

## 常用命令速查

### 生成矩阵
```bash
# Word矩阵
python scripts/generate_matrix.py

# Excel矩阵
python scripts/generate_excel_matrix.py
```

### 提取ROI数据
```bash
python scripts/extract_roi_data.py ./step2-选定场景深度调研/
```

### 生成ROI汇总
```bash
python scripts/roi_summary.py
```

### 运行测试
```bash
python tests/test_matrix_generation.py
python tests/test_roi_analysis.py
```

## 关键决策检查清单

- [ ] 是否完成了行业全景扫描？
- [ ] 是否构建了完整的竞品-场景矩阵？
- [ ] 是否标注了所有可切入场景？
- [ ] 是否对重点场景进行了深度调研？
- [ ] 是否完成了双视角ROI分析？
- [ ] 是否识别了平台化复用机会？
- [ ] 是否制定了分阶段切入路径？
- [ ] 是否给出了明确的Go/No-Go建议？

## 常见问题

**Q: 调研一个行业需要多长时间？**
A: 完整调研约需2-4周，具体时间取决于：
- 行业复杂度
- 可用资料丰富度
- 需要深度调研的场景数量

**Q: 如何确定要调研哪些场景？**
A: 先穷举所有可能的场景（通常30-50个），然后通过矩阵分析筛选出15-20个重点场景进行深度调研。

**Q: ROI估算的准确性如何？**
A: 客户视角ROI相对准确（基于公开数据），己方视角ROI基于假设参数，建议作为参考而非绝对依据。

**Q: 可以跳过某些阶段吗？**
A: 可以。如果时间紧迫，可以：
- 跳过Phase 1（如果已有行业认知）
- 减少Phase 4的深度调研场景数量
- 简化Phase 5的ROI分析

但建议至少完成Phase 2（矩阵分析）和Phase 6（路径规划）。
