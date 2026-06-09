# B端行业数字化可行性调研 Skill

一套经过验证的B端行业数字化产品线可行性调研方法论，帮助团队系统性地回答"要不要进入这个行业"、"哪些场景可以切入"、"每个场景值不值得做"以及"按什么路径推进"等关键问题。

## 适用场景

- "我们要不要进入XX行业做数字化产品？"
- "帮我调研一下XX行业的市场机会"
- "XX行业的竞品格局和可切入场景有哪些？"
- "生成XX行业的可行性调研报告"
- "评估在XX行业做SaaS/软件产品的可行性"

## 核心方法论

### 漏斗式递进 + 双视角决策

```
Phase 0: 调研准备
    ↓
Phase 1: 行业全景扫描（宽而浅）
    ↓
Phase 2: 竞品-场景交叉分析（识别机会空间）
    ↓
Phase 3: 场景筛选与聚焦（标注可切入场景）
    ↓
Phase 4: 单场景深度调研（窄而深）
    ↓
Phase 5: 投入产出双视角分析（客户ROI + 己方ROI）
    ↓
Phase 6: 路径规划与决策（Go/No-Go）
```

### 双视角ROI

- **客户视角**：客户采购方案后能获得的回报（用于售前说服）
- **己方视角**：我方研发生产该方案能获得的利润（用于内部决策）

## 配套脚本

| 脚本 | 功能 | 使用时机 |
|------|------|---------|
| `generate_matrix.py` | 生成竞品-场景交叉矩阵Word文档 | Phase 2 |
| `generate_excel_matrix.py` | 生成Excel版矩阵（含格式） | Phase 2 |
| `extract_roi_data.py` | 从深度调研文档批量提取ROI数据 | Phase 5.1 |
| `roi_summary.py` | 生成客户视角ROI汇总Excel | Phase 5.1 |
| `roi_analysis.py` | 生成己方视角ROI分析Excel | Phase 5.2 |

## 输出物清单

完成全部6个Phase后，应产出以下交付物：

| 阶段 | 交付物 | 格式 |
|------|--------|------|
| Phase 1 | [行业]全景扫描_调研框架_补充版 | Word |
| Phase 2 | [行业]竞品场景交叉矩阵表_完整版 | Word |
| Phase 2 | [行业]运营侧竞品场景矩阵_汇总表 | Excel |
| Phase 4 | [编号]_[场景名]_深度调研与售前方案 | Word × N |
| Phase 5.1 | [行业]场景投入产出比汇总对比 | Excel |
| Phase 5.2 | 己方视角投入产出分析 | Excel |
| Phase 6 | 切入路径规划与决策建议 | Word/PPT |

## 快速开始

### 1. 安装依赖

```bash
pip install python-docx openpyxl
```

### 2. 使用脚本

```python
# 生成竞品-场景交叉矩阵
from scripts.generate_matrix import build_matrix

scenes = [
    {"name": "智能巡检", "type": "生产运营", "pain_points": "人工巡检效率低"},
    # ... 更多场景
]

competitors = [
    {"name": "厂商A", "category": "行业龙头系"},
    # ... 更多竞品
]

build_matrix(industry="制造业", scenes=scenes, competitors=competitors)
```

### 3. 运行测试

```bash
cd tests
python test_matrix_generation.py
python test_roi_analysis.py
```

## 完整示例

参见 `references/example-electric-power.md`，了解电力行业调研的完整执行过程和关键决策点。

## 关键设计原则

1. **漏斗式递进**：先宽后深，避免过早聚焦导致方向性错误
2. **人机协作迭代**：AI生成初稿 → 用户审核反馈 → AI迭代补全
3. **矩阵化思维**：用"场景×竞品"交叉矩阵替代线性列表
4. **双视角决策**：同时考虑客户视角和己方视角ROI
5. **平台化思维**：识别跨场景复用的底层能力

## 注意事项

1. **数据时效性**：市场规模、竞品市占率等数据基于WebSearch获取，可能存在滞后
2. **ROI估算精度**：己方视角ROI基于假设参数，实际偏差可能较大，需结合团队实际情况校准
3. **行业深度**：AI对特定行业的认知深度有限，部分业务流程和技术细节可能不够准确
4. **WebSearch预算控制**：避免重复搜索，优先批量查询

## 项目结构

```
b2b-industry-research-skill/
├── SKILL.md                    # Skill主文件（方法论定义）
├── README.md                   # 本文件
├── scripts/                    # 配套脚本
│   ├── generate_matrix.py      # Word矩阵生成
│   ├── generate_excel_matrix.py # Excel矩阵生成
│   ├── extract_roi_data.py     # ROI数据提取
│   ├── roi_summary.py          # 客户视角ROI汇总
│   └── roi_analysis.py         # 己方视角ROI分析
├── references/                 # 参考文档
│   └── example-electric-power.md # 电力行业示例
└── tests/                      # 测试用例
    ├── test_matrix_generation.py
    └── test_roi_analysis.py
```

## License

MIT License
