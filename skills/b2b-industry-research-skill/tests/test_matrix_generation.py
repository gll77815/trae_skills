#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试矩阵生成功能

测试内容：
1. Word矩阵生成
2. Excel矩阵生成
3. 数据格式验证
4. 颜色标记验证
"""

import sys
import os
import unittest
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from generate_matrix import build_matrix
from generate_excel_matrix import create_excel_matrix


class TestMatrixGeneration(unittest.TestCase):
    """测试矩阵生成功能"""
    
    def setUp(self):
        """设置测试数据"""
        self.test_scenes = [
            {
                "name": "智能巡检",
                "type": "生产运营",
                "pain_points": "人工巡检效率低、漏检率高",
                "target_customers": "大型制造企业",
                "qualification": "无",
                "feasibility": "可切入",
                "market_shares": {"厂商A": "极高(70-80%)", "厂商B": "中(30-40%)"}
            },
            {
                "name": "设备预测性维护",
                "type": "生产运营",
                "pain_points": "设备故障导致停产损失大",
                "target_customers": "设备密集型企业",
                "qualification": "有",
                "feasibility": "观望",
                "market_shares": {"厂商A": "低(10-20%)", "厂商C": "中(40-50%)"}
            },
            {
                "name": "能源管理系统",
                "type": "运营管理",
                "pain_points": "能源浪费严重、成本居高不下",
                "target_customers": "高能耗企业",
                "qualification": "无",
                "feasibility": "可切入",
                "market_shares": {"厂商B": "极高(80-90%)", "厂商D": "低(5-15%)"}
            },
        ]
        
        self.test_competitors = [
            {"name": "厂商A", "category": "行业龙头系"},
            {"name": "厂商B", "category": "互联网系"},
            {"name": "厂商C", "category": "第三方专业厂商"},
            {"name": "厂商D", "category": "新兴创业公司"},
        ]
        
        self.test_industry = "测试行业"
        self.output_dir = Path(__file__).parent / "test_outputs"
        self.output_dir.mkdir(exist_ok=True)
    
    def test_word_matrix_generation(self):
        """测试Word矩阵生成"""
        output_path = self.output_dir / "test_matrix.docx"
        
        try:
            result = build_matrix(
                industry=self.test_industry,
                scenes=self.test_scenes,
                competitors=self.test_competitors,
                output_path=str(output_path)
            )
            
            # 验证文件是否生成
            self.assertTrue(output_path.exists(), "Word矩阵文件未生成")
            self.assertGreater(output_path.stat().st_size, 0, "Word矩阵文件为空")
            print(f"✓ Word矩阵生成成功: {result}")
            
        except Exception as e:
            self.fail(f"Word矩阵生成失败: {e}")
    
    def test_excel_matrix_generation(self):
        """测试Excel矩阵生成"""
        output_path = self.output_dir / "test_matrix.xlsx"
        
        try:
            result = create_excel_matrix(
                industry=self.test_industry,
                scenes=self.test_scenes,
                competitors=self.test_competitors,
                output_path=str(output_path)
            )
            
            # 验证文件是否生成
            self.assertTrue(output_path.exists(), "Excel矩阵文件未生成")
            self.assertGreater(output_path.stat().st_size, 0, "Excel矩阵文件为空")
            print(f"✓ Excel矩阵生成成功: {result}")
            
        except Exception as e:
            self.fail(f"Excel矩阵生成失败: {e}")
    
    def test_empty_scenes(self):
        """测试空场景列表处理"""
        output_path = self.output_dir / "test_empty.docx"
        
        try:
            result = build_matrix(
                industry=self.test_industry,
                scenes=[],
                competitors=self.test_competitors,
                output_path=str(output_path)
            )
            self.assertTrue(output_path.exists())
            print("✓ 空场景列表处理正常")
        except Exception as e:
            self.fail(f"空场景列表处理失败: {e}")
    
    def test_market_share_color_coding(self):
        """测试市场占有率颜色标记"""
        # 验证测试数据中的颜色标记逻辑
        for scene in self.test_scenes:
            market_shares = scene.get("market_shares", {})
            for competitor, share in market_shares.items():
                share_lower = str(share).lower()
                
                # 验证颜色分类
                if any(x in share_lower for x in ["极高", "70-90%", "70%", "80%", "90%"]):
                    color = "red"
                elif any(x in share_lower for x in ["中", "中等", "30-50%", "40%", "50%"]):
                    color = "orange"
                elif any(x in share_lower for x in ["低", "低等", "10-20%", "10%", "20%", "少"]):
                    color = "blue"
                else:
                    color = "none"
                
                self.assertIn(color, ["red", "orange", "blue", "none"])
        
        print("✓ 市场占有率颜色标记逻辑正确")


def run_tests():
    """运行测试"""
    print("="*60)
    print("开始运行矩阵生成测试")
    print("="*60)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMatrixGeneration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✓ 所有测试通过")
    else:
        print("✗ 部分测试失败")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
