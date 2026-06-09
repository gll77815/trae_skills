#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试ROI分析功能

测试内容：
1. ROI数据提取
2. ROI计算和评级
3. Excel生成
4. 边界条件处理
"""

import sys
import os
import unittest
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from roi_summary import (
    parse_payback_period,
    parse_roi_value,
    calculate_rating,
    get_recommendation_level,
    create_roi_summary_excel
)
from roi_analysis import create_customer_roi_excel, create_vendor_roi_excel


class TestROIParsing(unittest.TestCase):
    """测试ROI数据解析功能"""
    
    def test_parse_payback_period_months(self):
        """测试月份格式解析"""
        self.assertEqual(parse_payback_period("12个月"), 12)
        self.assertEqual(parse_payback_period("8个月"), 8)
        self.assertEqual(parse_payback_period("18个月"), 18)
        print("✓ 月份格式解析正确")
    
    def test_parse_payback_period_years(self):
        """测试年份格式解析"""
        self.assertEqual(parse_payback_period("1年"), 12)
        self.assertEqual(parse_payback_period("1.5年"), 18)
        self.assertEqual(parse_payback_period("2年"), 24)
        print("✓ 年份格式解析正确")
    
    def test_parse_payback_period_mixed(self):
        """测试混合格式解析"""
        self.assertEqual(parse_payback_period("1年3个月"), 15)
        self.assertEqual(parse_payback_period("2年6个月"), 30)
        print("✓ 混合格式解析正确")
    
    def test_parse_payback_period_edge_cases(self):
        """测试边界条件"""
        self.assertIsNone(parse_payback_period(""))
        self.assertIsNone(parse_payback_period(None))
        self.assertIsNone(parse_payback_period("未知"))
        print("✓ 边界条件处理正确")
    
    def test_parse_roi_percentage(self):
        """测试百分比格式解析"""
        self.assertEqual(parse_roi_value("300%"), 300)
        self.assertEqual(parse_roi_value("150%"), 150)
        print("✓ 百分比格式解析正确")
    
    def test_parse_roi_multiplier(self):
        """测试倍数格式解析"""
        self.assertEqual(parse_roi_value("3倍"), 300)
        self.assertEqual(parse_roi_value("2.5倍"), 250)
        self.assertEqual(parse_roi_value("3x"), 300)
        self.assertEqual(parse_roi_value("2.5X"), 250)
        print("✓ 倍数格式解析正确")


class TestROIRating(unittest.TestCase):
    """测试ROI评级功能"""
    
    def test_calculate_rating_five_star(self):
        """测试五星评级"""
        # 回收期 ≤ 12个月
        self.assertEqual(calculate_rating(8, None), "★★★★★")
        self.assertEqual(calculate_rating(12, None), "★★★★★")
        # 5年ROI ≥ 300%
        self.assertEqual(calculate_rating(None, 350), "★★★★★")
        print("✓ 五星评级计算正确")
    
    def test_calculate_rating_four_star(self):
        """测试四星评级"""
        self.assertEqual(calculate_rating(15, None), "★★★★☆")
        self.assertEqual(calculate_rating(None, 250), "★★★★☆")
        print("✓ 四星评级计算正确")
    
    def test_calculate_rating_three_star(self):
        """测试三星评级"""
        self.assertEqual(calculate_rating(20, None), "★★★☆☆")
        self.assertEqual(calculate_rating(None, 150), "★★★☆☆")
        print("✓ 三星评级计算正确")
    
    def test_calculate_rating_two_star(self):
        """测试二星评级"""
        self.assertEqual(calculate_rating(30, None), "★★☆☆☆")
        self.assertEqual(calculate_rating(None, 75), "★★☆☆☆")
        print("✓ 二星评级计算正确")
    
    def test_calculate_rating_unknown(self):
        """测试未知评级"""
        self.assertEqual(calculate_rating(None, None), "待评估")
        print("✓ 未知评级处理正确")
    
    def test_recommendation_level(self):
        """测试推荐梯队映射"""
        self.assertEqual(get_recommendation_level("★★★★★"), "强推")
        self.assertEqual(get_recommendation_level("★★★★☆"), "推荐")
        self.assertEqual(get_recommendation_level("★★★☆☆"), "可选")
        self.assertEqual(get_recommendation_level("★★☆☆☆"), "观望")
        self.assertEqual(get_recommendation_level("★☆☆☆☆"), "观望")
        self.assertEqual(get_recommendation_level("待评估"), "待评估")
        print("✓ 推荐梯队映射正确")


class TestROIExcelGeneration(unittest.TestCase):
    """测试ROI Excel生成功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_data = [
            {
                "scene_name": "智能巡检",
                "customer_investment": "50万元",
                "annual_benefit": "节省人工成本80万元/年",
                "payback_period": "8个月",
                "five_year_roi": "700%",
            },
            {
                "scene_name": "设备预测性维护",
                "customer_investment": "120万元",
                "annual_benefit": "减少停机损失200万元/年",
                "payback_period": "7个月",
                "five_year_roi": "733%",
            },
            {
                "scene_name": "能源管理系统",
                "customer_investment": "80万元",
                "annual_benefit": "节省能源成本30万元/年",
                "payback_period": "32个月",
                "five_year_roi": "87%",
            },
        ]
        
        self.output_dir = Path(__file__).parent / "test_outputs"
        self.output_dir.mkdir(exist_ok=True)
    
    def test_customer_roi_excel(self):
        """测试客户视角ROI Excel生成"""
        output_path = self.output_dir / "test_customer_roi.xlsx"
        
        try:
            result = create_roi_summary_excel(
                scenes_roi_data=self.test_data,
                industry="测试行业",
                output_path=str(output_path)
            )
            
            self.assertTrue(output_path.exists(), "Excel文件未生成")
            self.assertGreater(output_path.stat().st_size, 0, "Excel文件为空")
            print(f"✓ 客户视角ROI Excel生成成功: {result}")
            
        except Exception as e:
            self.fail(f"客户视角ROI Excel生成失败: {e}")
    
    def test_vendor_roi_excel(self):
        """测试己方视角ROI Excel生成"""
        output_path = self.output_dir / "test_vendor_roi.xlsx"
        
        test_scenarios = [
            {
                "name": "智能巡检",
                "rd_team_size": 8,
                "rd_duration_months": 6,
                "reusable_percentage": 40,
                "target_customers_3y": 50,
                "price_per_project": 500000,
                "delivery_cost": 200000,
            },
            {
                "name": "设备预测性维护",
                "rd_team_size": 12,
                "rd_duration_months": 9,
                "reusable_percentage": 30,
                "target_customers_3y": 30,
                "price_per_project": 1200000,
                "delivery_cost": 400000,
            },
        ]
        
        try:
            result = create_vendor_roi_excel(
                scenarios=test_scenarios,
                output_path=str(output_path)
            )
            
            self.assertTrue(output_path.exists(), "Excel文件未生成")
            self.assertGreater(output_path.stat().st_size, 0, "Excel文件为空")
            print(f"✓ 己方视角ROI Excel生成成功: {result}")
            
        except Exception as e:
            self.fail(f"己方视角ROI Excel生成失败: {e}")
    
    def test_empty_data(self):
        """测试空数据处理"""
        output_path = self.output_dir / "test_empty_roi.xlsx"
        
        try:
            result = create_roi_summary_excel(
                scenes_roi_data=[],
                industry="测试行业",
                output_path=str(output_path)
            )
            self.assertTrue(output_path.exists())
            print("✓ 空数据处理正常")
        except Exception as e:
            self.fail(f"空数据处理失败: {e}")


def run_tests():
    """运行测试"""
    print("="*60)
    print("开始运行ROI分析测试")
    print("="*60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestROIParsing))
    suite.addTests(loader.loadTestsFromTestCase(TestROIRating))
    suite.addTests(loader.loadTestsFromTestCase(TestROIExcelGeneration))
    
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
