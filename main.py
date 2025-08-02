#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能股票分析系统 - 主启动脚本

使用方法:
1. GUI模式（推荐）: python main.py
2. 命令行模式: python main.py --cli
3. 演示模式: python main.py --demo
4. 帮助信息: python main.py --help
"""

import sys
import argparse
import os
from datetime import datetime

def check_dependencies():
    """检查依赖包是否安装"""
    required_packages = {
        'akshare': 'akshare',
        'baostock': 'baostock', 
        'pandas': 'pandas',
        'numpy': 'numpy',
        'matplotlib': 'matplotlib'
    }
    
    optional_packages = {
        'seaborn': 'seaborn'
    }
    
    missing_packages = []
    missing_optional = []
    
    # 检查必需依赖
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    # 检查可选依赖
    for package_name, import_name in optional_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_optional.append(package_name)
    
    if missing_packages:
        print("❌ 缺少以下必需依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n请运行以下命令安装依赖:")
        print(f"pip install {' '.join(missing_packages)}")
        print("\n或者运行:")
        print("pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print("⚠️ 缺少以下可选依赖包（不影响核心功能）:")
        for package in missing_optional:
            print(f"   - {package}")
        print("\n如需完整功能，可运行:")
        print(f"pip install {' '.join(missing_optional)}")
    
    print("✅ 核心依赖包已安装")
    return True

def run_gui():
    """运行GUI界面"""
    try:
        print("🚀 启动图形界面...")
        from stock_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ 导入GUI模块失败: {e}")
        print("请确保 stock_gui.py 文件存在")
        return False
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")
        return False
    return True

def run_cli():
    """运行命令行界面"""
    try:
        from stock_analyzer import StockAnalyzer
        
        print("=== 智能股票分析系统 - 命令行模式 ===")
        print("正在初始化分析器...")
        
        analyzer = StockAnalyzer()
        
        while True:
            print("\n请选择功能:")
            print("1. 智能选股")
            print("2. 个股分析")
            print("3. 退出")
            
            choice = input("\n请输入选项 (1-3): ").strip()
            
            if choice == '1':
                rule_text = input("\n请输入选股规则（自然语言）: ").strip()
                if rule_text:
                    try:
                        limit = int(input("最大结果数 (默认50): ") or "50")
                        print(f"\n正在筛选股票，规则: {rule_text}")
                        stocks = analyzer.screen_stocks_by_rule(rule_text, limit)
                        report = analyzer.generate_report(stocks)
                        print(report)
                        
                        # 询问是否保存结果
                        save = input("\n是否保存结果到文件? (y/n): ").strip().lower()
                        if save == 'y':
                            filename = f"screening_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(report)
                            print(f"结果已保存到: {filename}")
                    except Exception as e:
                        print(f"筛选失败: {e}")
            
            elif choice == '2':
                stock_code = input("\n请输入股票代码: ").strip()
                if stock_code:
                    try:
                        days = int(input("分析天数 (默认60): ") or "60")
                        print(f"\n正在分析股票: {stock_code}")
                        stock_data = analyzer.analyze_stock(stock_code, days)
                        
                        if stock_data:
                            print(f"\n=== {stock_data.name}({stock_data.symbol}) 分析结果 ===")
                            print(f"当前价格: {stock_data.current_price}元")
                            print(f"涨跌幅: {stock_data.change_pct}%")
                            print(f"市值: {stock_data.market_cap/100000000:.2f}亿元")
                            print(f"PE: {stock_data.pe_ratio:.2f}" if stock_data.pe_ratio > 0 else "PE: --")
                            print(f"PB: {stock_data.pb_ratio:.2f}" if stock_data.pb_ratio > 0 else "PB: --")
                            
                            # 技术指标简要信息
                            if stock_data.technical_indicators:
                                print("\n技术指标:")
                                if 'rsi' in stock_data.technical_indicators:
                                    rsi = stock_data.technical_indicators['rsi'].iloc[-1]
                                    print(f"RSI: {rsi:.2f}")
                                if 'ma5' in stock_data.technical_indicators:
                                    ma5 = stock_data.technical_indicators['ma5'].iloc[-1]
                                    print(f"5日均线: {ma5:.2f}元")
                        else:
                            print("分析失败，无法获取股票数据")
                    except Exception as e:
                        print(f"分析失败: {e}")
            
            elif choice == '3':
                print("感谢使用！")
                break
            
            else:
                print("无效选项，请重新输入")
    
    except Exception as e:
        print(f"❌ 命令行模式启动失败: {e}")
        return False
    
    return True

def run_demo():
    """运行演示模式"""
    try:
        print("🎯 启动演示模式...")
        from stock_analyzer import main as demo_main
        demo_main()
    except Exception as e:
        print(f"❌ 演示模式启动失败: {e}")
        return False
    return True

def show_help():
    """显示帮助信息"""
    help_text = """
🏆 智能股票分析系统

功能特点:
✅ 支持自然语言选股规则
✅ 整合AKShare和BaoStock数据源
✅ 丰富的技术指标分析
✅ 直观的图形界面
✅ 数据导出功能

使用方法:
  python main.py           # 启动GUI界面（推荐）
  python main.py --gui     # 启动GUI界面
  python main.py --cli     # 启动命令行界面
  python main.py --demo    # 运行功能演示
  python main.py --help    # 显示帮助信息

选股规则示例:
  "股价大于10元且涨幅大于3%"
  "市值大于50亿且PE小于30"
  "RSI在30到70之间且股价站上20日均线"
  "涨幅大于5%且成交量大于1000万手"

技术支持:
  如遇问题，请检查:
  1. Python版本 >= 3.7
  2. 依赖包是否完整安装
  3. 网络连接是否正常

项目文件:
  main.py           - 主启动脚本
  stock_analyzer.py - 核心分析引擎
  stock_gui.py      - 图形界面
  requirements.txt  - 依赖包列表
"""
    print(help_text)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='智能股票分析系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用示例:
  python main.py           # GUI模式
  python main.py --cli     # 命令行模式
  python main.py --demo    # 演示模式"""
    )
    
    parser.add_argument('--gui', action='store_true', help='启动GUI界面')
    parser.add_argument('--cli', action='store_true', help='启动命令行界面')
    parser.add_argument('--demo', action='store_true', help='运行演示模式')
    parser.add_argument('--check', action='store_true', help='检查依赖包')
    
    args = parser.parse_args()
    
    # 显示欢迎信息
    print("\n" + "="*50)
    print("🏆 智能股票分析系统")
    print("   AI-Powered Stock Analysis System")
    print("="*50)
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 根据参数选择运行模式
    if args.check:
        print("\n✅ 依赖检查完成")
        return 0
    elif args.cli:
        success = run_cli()
    elif args.demo:
        success = run_demo()
    elif args.gui or len(sys.argv) == 1:  # 默认启动GUI
        success = run_gui()
    else:
        show_help()
        return 0
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序异常退出: {e}")
        sys.exit(1)