#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析系统图形界面
提供用户友好的GUI界面进行股票分析和选股
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime
import os
from stock_analyzer import StockAnalyzer, StockData
from typing import List

class StockAnalysisGUI:
    """股票分析系统GUI主类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("智能股票分析系统")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # 初始化分析器
        self.analyzer = None
        self.current_stocks = []
        self.current_analysis_stock = None
        
        # 创建界面
        self.create_widgets()
        
        # 初始化分析器（在后台线程中）
        self.init_analyzer()
    
    def create_widgets(self):
        """创建GUI组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="智能股票分析系统", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 左侧控制面板
        self.create_control_panel(main_frame)
        
        # 右侧结果显示区域
        self.create_result_panel(main_frame)
        
        # 底部状态栏
        self.create_status_bar(main_frame)
    
    def create_control_panel(self, parent):
        """创建左侧控制面板"""
        control_frame = ttk.LabelFrame(parent, text="控制面板", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 选股规则输入区域
        rule_frame = ttk.LabelFrame(control_frame, text="智能选股", padding="10")
        rule_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(rule_frame, text="请输入选股规则（自然语言）:").pack(anchor=tk.W)
        
        # 规则输入文本框
        self.rule_text = scrolledtext.ScrolledText(rule_frame, height=4, width=40)
        self.rule_text.pack(fill=tk.X, pady=(5, 10))
        
        # 预设规则按钮
        preset_frame = ttk.Frame(rule_frame)
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(preset_frame, text="快速选择:").pack(anchor=tk.W)
        
        preset_rules = [
            "股价大于10元且涨幅大于3%",
            "市值大于50亿且PE小于30",
            "RSI在30到70之间且股价站上20日均线",
            "涨幅大于5%且成交量大于1000万手"
        ]
        
        for rule in preset_rules:
            btn = ttk.Button(preset_frame, text=rule[:20] + "...", 
                           command=lambda r=rule: self.set_rule_text(r))
            btn.pack(fill=tk.X, pady=1)
        
        # 筛选参数
        param_frame = ttk.Frame(rule_frame)
        param_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(param_frame, text="最大结果数:").pack(side=tk.LEFT)
        self.limit_var = tk.StringVar(value="50")
        limit_entry = ttk.Entry(param_frame, textvariable=self.limit_var, width=10)
        limit_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        # 筛选按钮
        self.screen_btn = ttk.Button(rule_frame, text="开始筛选", 
                                   command=self.start_screening)
        self.screen_btn.pack(fill=tk.X, pady=(10, 0))
        
        # 个股分析区域
        analysis_frame = ttk.LabelFrame(control_frame, text="个股分析", padding="10")
        analysis_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(analysis_frame, text="股票代码:").pack(anchor=tk.W)
        
        code_frame = ttk.Frame(analysis_frame)
        code_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.stock_code_var = tk.StringVar()
        code_entry = ttk.Entry(code_frame, textvariable=self.stock_code_var)
        code_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.analyze_btn = ttk.Button(code_frame, text="分析", 
                                    command=self.start_stock_analysis)
        self.analyze_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 分析天数
        days_frame = ttk.Frame(analysis_frame)
        days_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(days_frame, text="分析天数:").pack(side=tk.LEFT)
        self.days_var = tk.StringVar(value="60")
        days_entry = ttk.Entry(days_frame, textvariable=self.days_var, width=10)
        days_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # 导出功能
        export_frame = ttk.LabelFrame(control_frame, text="导出功能", padding="10")
        export_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.export_btn = ttk.Button(export_frame, text="导出筛选结果", 
                                   command=self.export_results, state=tk.DISABLED)
        self.export_btn.pack(fill=tk.X)
    
    def create_result_panel(self, parent):
        """创建右侧结果显示面板"""
        # 创建Notebook用于标签页
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          pady=(0, 10))
        
        # 筛选结果标签页
        self.create_screening_tab()
        
        # 个股分析标签页
        self.create_analysis_tab()
        
        # 技术图表标签页
        self.create_chart_tab()
    
    def create_screening_tab(self):
        """创建筛选结果标签页"""
        screening_frame = ttk.Frame(self.notebook)
        self.notebook.add(screening_frame, text="筛选结果")
        
        # 结果表格
        columns = ('代码', '名称', '现价', '涨跌幅', '成交量', '市值(亿)', 'PE', 'PB')
        self.result_tree = ttk.Treeview(screening_frame, columns=columns, show='headings')
        
        # 设置列标题和宽度
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=80, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(screening_frame, orient=tk.VERTICAL, 
                                   command=self.result_tree.yview)
        scrollbar_x = ttk.Scrollbar(screening_frame, orient=tk.HORIZONTAL, 
                                   command=self.result_tree.xview)
        self.result_tree.configure(yscrollcommand=scrollbar_y.set, 
                                  xscrollcommand=scrollbar_x.set)
        
        # 布局
        self.result_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        screening_frame.columnconfigure(0, weight=1)
        screening_frame.rowconfigure(0, weight=1)
        
        # 双击事件
        self.result_tree.bind('<Double-1>', self.on_stock_double_click)
    
    def create_analysis_tab(self):
        """创建个股分析标签页"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="个股分析")
        
        # 分析结果文本框
        self.analysis_text = scrolledtext.ScrolledText(analysis_frame, 
                                                      font=('Consolas', 10))
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_chart_tab(self):
        """创建技术图表标签页"""
        chart_frame = ttk.Frame(self.notebook)
        self.notebook.add(chart_frame, text="技术图表")
        
        # 创建matplotlib图表
        self.fig = Figure(figsize=(12, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 图表工具栏
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(self.canvas, chart_frame)
        toolbar.update()
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("正在初始化分析器...")
        
        status_bar = ttk.Label(parent, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                       pady=(10, 0))
    
    def init_analyzer(self):
        """在后台线程中初始化分析器"""
        def init_thread():
            try:
                self.status_var.set("正在初始化数据接口...")
                self.analyzer = StockAnalyzer()
                self.status_var.set("系统就绪")
                
                # 启用按钮
                self.screen_btn.configure(state=tk.NORMAL)
                self.analyze_btn.configure(state=tk.NORMAL)
            except Exception as e:
                self.status_var.set(f"初始化失败: {str(e)}")
                messagebox.showerror("错误", f"系统初始化失败:\n{str(e)}")
        
        thread = threading.Thread(target=init_thread, daemon=True)
        thread.start()
    
    def set_rule_text(self, rule):
        """设置规则文本"""
        self.rule_text.delete(1.0, tk.END)
        self.rule_text.insert(1.0, rule)
    
    def start_screening(self):
        """开始筛选股票"""
        if not self.analyzer:
            messagebox.showwarning("警告", "分析器尚未初始化完成")
            return
        
        rule_text = self.rule_text.get(1.0, tk.END).strip()
        if not rule_text:
            messagebox.showwarning("警告", "请输入筛选规则")
            return
        
        try:
            limit = int(self.limit_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return
        
        # 在后台线程中执行筛选
        def screening_thread():
            try:
                self.status_var.set("正在筛选股票...")
                self.screen_btn.configure(state=tk.DISABLED)
                
                stocks = self.analyzer.screen_stocks_by_rule(rule_text, limit)
                
                # 在主线程中更新UI
                self.root.after(0, self.update_screening_results, stocks)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"筛选失败:\n{str(e)}"))
            finally:
                self.root.after(0, lambda: self.screen_btn.configure(state=tk.NORMAL))
                self.root.after(0, lambda: self.status_var.set("筛选完成"))
        
        thread = threading.Thread(target=screening_thread, daemon=True)
        thread.start()
    
    def update_screening_results(self, stocks: List[StockData]):
        """更新筛选结果显示"""
        # 清空现有结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        # 添加新结果
        self.current_stocks = stocks
        for stock in stocks:
            market_cap_yi = stock.market_cap / 100000000 if stock.market_cap > 0 else 0
            volume_wan = stock.volume / 10000 if stock.volume > 0 else 0
            
            self.result_tree.insert('', tk.END, values=(
                stock.symbol,
                stock.name,
                f"{stock.current_price:.2f}",
                f"{stock.change_pct:.2f}%",
                f"{volume_wan:.0f}万",
                f"{market_cap_yi:.2f}",
                f"{stock.pe_ratio:.2f}" if stock.pe_ratio > 0 else "--",
                f"{stock.pb_ratio:.2f}" if stock.pb_ratio > 0 else "--"
            ))
        
        # 启用导出按钮
        if stocks:
            self.export_btn.configure(state=tk.NORMAL)
        
        # 切换到筛选结果标签页
        self.notebook.select(0)
        
        self.status_var.set(f"找到 {len(stocks)} 只符合条件的股票")
    
    def start_stock_analysis(self):
        """开始个股分析"""
        if not self.analyzer:
            messagebox.showwarning("警告", "分析器尚未初始化完成")
            return
        
        stock_code = self.stock_code_var.get().strip()
        if not stock_code:
            messagebox.showwarning("警告", "请输入股票代码")
            return
        
        try:
            days = int(self.days_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的天数")
            return
        
        # 在后台线程中执行分析
        def analysis_thread():
            try:
                self.status_var.set(f"正在分析股票 {stock_code}...")
                self.analyze_btn.configure(state=tk.DISABLED)
                
                stock_data = self.analyzer.analyze_stock(stock_code, days)
                
                # 在主线程中更新UI
                self.root.after(0, self.update_analysis_results, stock_data)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"分析失败:\n{str(e)}"))
            finally:
                self.root.after(0, lambda: self.analyze_btn.configure(state=tk.NORMAL))
                self.root.after(0, lambda: self.status_var.set("分析完成"))
        
        thread = threading.Thread(target=analysis_thread, daemon=True)
        thread.start()
    
    def update_analysis_results(self, stock_data: StockData):
        """更新个股分析结果"""
        if not stock_data:
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, "无法获取股票数据")
            return
        
        # 生成分析报告
        report = self.generate_stock_report(stock_data)
        
        # 更新文本框
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, report)
        
        # 更新图表
        self.update_stock_chart(stock_data)
        
        # 保存当前分析的股票
        self.current_analysis_stock = stock_data
        
        # 切换到分析标签页
        self.notebook.select(1)
    
    def generate_stock_report(self, stock_data: StockData) -> str:
        """生成股票分析报告"""
        report = f"\n=== {stock_data.name}({stock_data.symbol}) 分析报告 ===\n"
        report += f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 基本信息
        report += "基本信息:\n"
        report += f"  当前价格: {stock_data.current_price:.2f} 元\n"
        report += f"  涨跌幅: {stock_data.change_pct:.2f}%\n"
        report += f"  成交量: {stock_data.volume/10000:.0f} 万手\n"
        report += f"  市值: {stock_data.market_cap/100000000:.2f} 亿元\n"
        report += f"  市盈率: {stock_data.pe_ratio:.2f}\n" if stock_data.pe_ratio > 0 else "  市盈率: --\n"
        report += f"  市净率: {stock_data.pb_ratio:.2f}\n" if stock_data.pb_ratio > 0 else "  市净率: --\n"
        
        # 技术指标分析
        if stock_data.technical_indicators:
            report += "\n技术指标分析:\n"
            
            # MA分析
            if 'ma5' in stock_data.technical_indicators and 'ma20' in stock_data.technical_indicators:
                ma5_current = stock_data.technical_indicators['ma5'].iloc[-1]
                ma20_current = stock_data.technical_indicators['ma20'].iloc[-1]
                
                report += f"  5日均线: {ma5_current:.2f} 元\n"
                report += f"  20日均线: {ma20_current:.2f} 元\n"
                
                if stock_data.current_price > ma5_current:
                    report += "  ✓ 股价站上5日均线\n"
                else:
                    report += "  ✗ 股价跌破5日均线\n"
                
                if stock_data.current_price > ma20_current:
                    report += "  ✓ 股价站上20日均线\n"
                else:
                    report += "  ✗ 股价跌破20日均线\n"
            
            # RSI分析
            if 'rsi' in stock_data.technical_indicators:
                rsi_current = stock_data.technical_indicators['rsi'].iloc[-1]
                report += f"  RSI: {rsi_current:.2f}\n"
                
                if rsi_current > 70:
                    report += "  ⚠ RSI超买信号\n"
                elif rsi_current < 30:
                    report += "  ⚠ RSI超卖信号\n"
                else:
                    report += "  ✓ RSI处于正常区间\n"
            
            # MACD分析
            if 'macd' in stock_data.technical_indicators:
                macd_data = stock_data.technical_indicators['macd']
                macd_current = macd_data['macd'].iloc[-1]
                signal_current = macd_data['signal'].iloc[-1]
                histogram_current = macd_data['histogram'].iloc[-1]
                
                report += f"  MACD: {macd_current:.4f}\n"
                report += f"  Signal: {signal_current:.4f}\n"
                
                if macd_current > signal_current:
                    report += "  ✓ MACD金叉信号\n"
                else:
                    report += "  ✗ MACD死叉信号\n"
        
        # 历史数据统计
        if not stock_data.historical_data.empty:
            hist_data = stock_data.historical_data
            close_prices = pd.to_numeric(hist_data['收盘'], errors='coerce')
            
            report += "\n历史数据统计:\n"
            report += f"  数据天数: {len(hist_data)} 天\n"
            report += f"  最高价: {close_prices.max():.2f} 元\n"
            report += f"  最低价: {close_prices.min():.2f} 元\n"
            report += f"  平均价: {close_prices.mean():.2f} 元\n"
            report += f"  价格波动率: {close_prices.std():.2f}\n"
        
        return report
    
    def update_stock_chart(self, stock_data: StockData):
        """更新股票技术图表"""
        if stock_data.historical_data.empty:
            return
        
        # 清空现有图表
        self.fig.clear()
        
        # 准备数据
        hist_data = stock_data.historical_data.copy()
        hist_data['日期'] = pd.to_datetime(hist_data['日期'])
        hist_data.set_index('日期', inplace=True)
        
        close_prices = pd.to_numeric(hist_data['收盘'], errors='coerce')
        
        # 创建子图
        ax1 = self.fig.add_subplot(3, 1, 1)
        ax2 = self.fig.add_subplot(3, 1, 2)
        ax3 = self.fig.add_subplot(3, 1, 3)
        
        # 第一个子图：价格和移动平均线
        ax1.plot(hist_data.index, close_prices, label='收盘价', linewidth=2, color='blue')
        if 'ma5' in stock_data.technical_indicators:
            ax1.plot(hist_data.index, stock_data.technical_indicators['ma5'], 
                    label='MA5', alpha=0.7, color='orange')
        if 'ma20' in stock_data.technical_indicators:
            ax1.plot(hist_data.index, stock_data.technical_indicators['ma20'], 
                    label='MA20', alpha=0.7, color='green')
        
        ax1.set_title(f'{stock_data.name}({stock_data.symbol}) 股价走势与移动平均线')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 第二个子图：RSI
        if 'rsi' in stock_data.technical_indicators:
            rsi = stock_data.technical_indicators['rsi']
            ax2.plot(hist_data.index, rsi, label='RSI', color='purple')
            ax2.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='超买线(70)')
            ax2.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='超卖线(30)')
            ax2.set_title('RSI相对强弱指数')
            ax2.set_ylim(0, 100)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        # 第三个子图：MACD
        if 'macd' in stock_data.technical_indicators:
            macd_data = stock_data.technical_indicators['macd']
            ax3.plot(hist_data.index, macd_data['macd'], label='MACD', color='blue')
            ax3.plot(hist_data.index, macd_data['signal'], label='Signal', color='red')
            ax3.bar(hist_data.index, macd_data['histogram'], label='Histogram', 
                   alpha=0.6, color='gray', width=1)
            ax3.set_title('MACD指标')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        # 调整布局
        self.fig.tight_layout()
        
        # 刷新画布
        self.canvas.draw()
        
        # 切换到图表标签页
        self.notebook.select(2)
    
    def on_stock_double_click(self, event):
        """双击股票列表项时的处理"""
        selection = self.result_tree.selection()
        if selection:
            item = self.result_tree.item(selection[0])
            stock_code = item['values'][0]
            
            # 设置股票代码并开始分析
            self.stock_code_var.set(stock_code)
            self.start_stock_analysis()
    
    def export_results(self):
        """导出筛选结果"""
        if not self.current_stocks:
            messagebox.showwarning("警告", "没有可导出的数据")
            return
        
        # 选择保存文件
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            # 准备数据
            data = []
            for stock in self.current_stocks:
                data.append({
                    '代码': stock.symbol,
                    '名称': stock.name,
                    '现价': stock.current_price,
                    '涨跌幅(%)': stock.change_pct,
                    '成交量(万手)': stock.volume / 10000,
                    '市值(亿元)': stock.market_cap / 100000000,
                    'PE': stock.pe_ratio if stock.pe_ratio > 0 else None,
                    'PB': stock.pb_ratio if stock.pb_ratio > 0 else None,
                    '导出时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            df = pd.DataFrame(data)
            
            # 根据文件扩展名选择保存格式
            if filename.endswith('.xlsx'):
                df.to_excel(filename, index=False)
            else:
                df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            messagebox.showinfo("成功", f"数据已导出到:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败:\n{str(e)}")

def main():
    """主函数"""
    root = tk.Tk()
    app = StockAnalysisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()