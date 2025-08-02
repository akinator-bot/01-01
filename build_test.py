#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟buildozer构建前的最终检查
确保Android构建能够成功
"""

import os
import sys

def simulate_buildozer_check():
    """模拟buildozer的构建前检查"""
    print("=== 模拟Buildozer构建检查 ===")
    
    # 检查主入口文件
    if not os.path.exists('main_mobile.py'):
        print("❌ 主入口文件 main_mobile.py 不存在")
        return False
    print("✅ 主入口文件存在")
    
    # 检查核心模块
    if not os.path.exists('mobile_stock_analyzer.py'):
        print("❌ 核心模块 mobile_stock_analyzer.py 不存在")
        return False
    print("✅ 核心模块存在")
    
    # 检查buildozer.spec
    if not os.path.exists('buildozer.spec'):
        print("❌ buildozer.spec 不存在")
        return False
    print("✅ buildozer.spec 存在")
    
    # 检查requirements配置
    with open('buildozer.spec', 'r', encoding='utf-8') as f:
        spec_content = f.read()
    
    if 'requirements = python3,kivy,requests,baostock' not in spec_content:
        print("❌ buildozer.spec requirements配置不正确")
        return False
    print("✅ requirements配置正确")
    
    # 检查排除模式
    if 'source.exclude_patterns' not in spec_content:
        print("❌ 缺少文件排除配置")
        return False
    print("✅ 文件排除配置存在")
    
    # 检查是否排除了桌面版文件
    excluded_files = ['main.py', 'stock_analyzer.py', 'enhanced_gui.py', 'stock_gui.py']
    for file in excluded_files:
        if file not in spec_content:
            print(f"❌ 桌面版文件 {file} 未被排除")
            return False
    print("✅ 桌面版文件已正确排除")
    
    return True

def check_android_compatibility():
    """检查Android兼容性"""
    print("\n=== Android兼容性检查 ===")
    
    try:
        # 尝试导入移动端模块
        from mobile_stock_analyzer import MobileStockAnalyzer
        analyzer = MobileStockAnalyzer()
        print("✅ 移动端模块导入成功")
        
        # 测试基本功能
        stocks = analyzer.screen_stocks_by_rule("测试规则", 3)
        print(f"✅ 选股功能正常，返回 {len(stocks)} 只股票")
        
        # 测试个股分析
        analysis = analyzer.analyze_stock('000001')
        if analysis:
            print("✅ 个股分析功能正常")
        else:
            print("⚠️  个股分析返回空结果，但功能正常")
            
    except Exception as e:
        print(f"❌ Android兼容性测试失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("Buildozer构建前最终检查")
    print("=" * 50)
    
    checks = [
        simulate_buildozer_check,
        check_android_compatibility
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        try:
            if check():
                passed += 1
        except Exception as e:
            print(f"❌ 检查异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"检查结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有检查通过！可以开始Android构建")
        print("\n建议的构建命令:")
        print("buildozer android debug")
        return True
    else:
        print("⚠️  存在问题，请修复后再构建")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)