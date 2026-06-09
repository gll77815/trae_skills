#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从深度调研文档批量提取ROI数据

功能：
1. 遍历指定文件夹中的所有Word文档
2. 提取每个场景的ROI相关数据
3. 汇总为结构化数据供后续分析

使用时机：Phase 5.1 - 客户视角ROI分析
"""

import os
import re
from pathlib import Path


def extract_roi_from_docx(docx_path):
    """
    从单个Word文档中提取ROI数据
    
    参数:
        docx_path: Word文档路径
    
    返回:
        dict: 包含场景名称和ROI数据的字典
    """
    
    try:
        from docx import Document
    except ImportError:
        print("请先安装python-docx: pip install python-docx")
        return None
    
    doc = Document(docx_path)
    
    # 初始化数据
    roi_data = {
        "scene_name": "",
        "customer_investment": "",  # 客户投入
        "annual_benefit": "",       # 年收益
        "payback_period": "",       # 回收期
        "five_year_roi": "",        # 5年ROI
        "data_source": str(docx_path)
    }
    
    # 从文件名提取场景名称
    filename = os.path.basename(docx_path)
    # 移除编号前缀和扩展名
    scene_name = re.sub(r'^\d+_', '', filename)
    scene_name = scene_name.replace('_深度调研与售前方案.docx', '')
    scene_name = scene_name.replace('.docx', '')
    roi_data["scene_name"] = scene_name
    
    # 遍历文档段落提取ROI信息
    full_text = "\n".join([para.text for para in doc.paragraphs])
    
    # 提取客户投入
    investment_patterns = [
        r'客户投入[：:]\s*([^\n]+)',
        r'初期投资[：:]\s*([^\n]+)',
        r'采购成本[：:]\s*([^\n]+)',
        r'投入成本[：:]\s*([^\n]+)',
    ]
    for pattern in investment_patterns:
        match = re.search(pattern, full_text)
        if match:
            roi_data["customer_investment"] = match.group(1).strip()
            break
    
    # 提取年收益
    benefit_patterns = [
        r'年收益[：:]\s*([^\n]+)',
        r'年度收益[：:]\s*([^\n]+)',
        r'年节省[：:]\s*([^\n]+)',
        r'年回报[：:]\s*([^\n]+)',
    ]
    for pattern in benefit_patterns:
        match = re.search(pattern, full_text)
        if match:
            roi_data["annual_benefit"] = match.group(1).strip()
            break
    
    # 提取回收期
    payback_patterns = [
        r'回收期[：:]\s*([^\n]+)',
        r'投资回收期[：:]\s*([^\n]+)',
        r'([0-9.]+)\s*个月?回收',
        r'([0-9.]+)\s*年?回收',
    ]
    for pattern in payback_patterns:
        match = re.search(pattern, full_text)
        if match:
            roi_data["payback_period"] = match.group(1).strip()
            break
    
    # 提取5年ROI
    roi_patterns = [
        r'5年ROI[：:]\s*([^\n]+)',
        r'五年ROI[：:]\s*([^\n]+)',
        r'ROI[：:]\s*([^\n]+)',
        r'投资回报率[：:]\s*([^\n]+)',
    ]
    for pattern in roi_patterns:
        match = re.search(pattern, full_text)
        if match:
            roi_data["five_year_roi"] = match.group(1).strip()
            break
    
    return roi_data


def extract_all_roi_data(folder_path, output_format="dict"):
    """
    从文件夹中所有文档提取ROI数据
    
    参数:
        folder_path: 包含深度调研文档的文件夹路径
        output_format: 输出格式 ("dict" 或 "list")
    
    返回:
        list或dict: 所有场景的ROI数据
    """
    
    folder = Path(folder_path)
    roi_data_list = []
    
    # 遍历所有docx文件
    for docx_file in folder.glob("*.docx"):
        print(f"正在处理: {docx_file.name}")
        roi_data = extract_roi_from_docx(str(docx_file))
        if roi_data:
            roi_data_list.append(roi_data)
    
    if output_format == "dict":
        # 转换为以场景名为key的字典
        return {item["scene_name"]: item for item in roi_data_list}
    
    return roi_data_list


def save_roi_to_json(roi_data, output_path):
    """保存ROI数据为JSON文件"""
    import json
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(roi_data, f, ensure_ascii=False, indent=2)
    print(f"ROI数据已保存: {output_path}")


def print_roi_summary(roi_data):
    """打印ROI数据摘要"""
    print("\n" + "="*80)
    print("ROI数据提取摘要")
    print("="*80)
    
    for item in roi_data:
        print(f"\n场景: {item['scene_name']}")
        print(f"  客户投入: {item['customer_investment'] or '未提取'}")
        print(f"  年收益: {item['annual_benefit'] or '未提取'}")
        print(f"  回收期: {item['payback_period'] or '未提取'}")
        print(f"  5年ROI: {item['five_year_roi'] or '未提取'}")


def main():
    """示例用法"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python extract_roi_data.py <文件夹路径>")
        print("示例: python extract_roi_data.py ./step2-选定场景深度调研/")
        return
    
    folder_path = sys.argv[1]
    
    if not os.path.exists(folder_path):
        print(f"错误: 文件夹不存在 {folder_path}")
        return
    
    # 提取数据
    roi_data = extract_all_roi_data(folder_path, output_format="list")
    
    # 打印摘要
    print_roi_summary(roi_data)
    
    # 保存为JSON
    output_json = os.path.join(folder_path, "extracted_roi_data.json")
    save_roi_to_json(roi_data, output_json)


if __name__ == "__main__":
    main()
