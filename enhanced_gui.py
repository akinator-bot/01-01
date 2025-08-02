#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版股票分析系统GUI
集成改进的自然语言处理和更丰富的功能
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
import json
from stock_analyzer import StockAnalyzer, StockData
from enhanced_nlp_parser import EnhancedNLPParser
from typing import List, Dict

class EnhancedStockGUI:
    """增强版股票分析系统GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 智能股票分析系统 - 增强版")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f5f5f5')
        
        # 设置样式
        self.setup_styles()
        
        # 初始化组件
        self.analyzer = None
        self.enhanced_parser = EnhancedNLPParser()
        self.current_stocks = []
        self.current_analysis_stock = None
        self.rule_history = []
        
        # 创建界面
        self.create_widgets()
        
        # 初始化分析器
        self.init_analyzer()
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        
        # 配置样式主题
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Success.TLabel', foreground='#27ae60')
        style.configure('Warning.TLabel', foreground='#e67e22')
        style.configure('Error.TLabel', foreground='#e74c3c')
        
        # 按钮样式
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        style.configure('Success.TButton', font=('Arial', 10, 'bold'))
        
        # 设置颜色主题
        style.configure('TNotebook', background='#ecf0f1')
        style.configure('TNotebook.Tab', padding=[20, 8])
    
    def create_widgets(self):
        """创建GUI组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题区域
        self.create_header(main_frame)
        
        # 左侧控制面板
        self.create_enhanced_control_panel(main_frame)
        
        # 右侧结果显示区域
        self.create_enhanced_result_panel(main_frame)
        
        # 底部状态栏
        self.create_enhanced_status_bar(main_frame)
    
    def create_header(self, parent):
        """创建标题区域"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # 主标题
        title_label = ttk.Label(header_frame, text="🚀 智能股票分析系统", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # 版本信息
        version_label = ttk.Label(header_frame, text="增强版 v2.0", 
                                 font=('Arial', 10), foreground='#7f8c8d')
        version_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 右侧功能按钮
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="💾 保存配置", 
                  command=self.save_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="📂 加载配置", 
                  command=self.load_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="❓ 帮助", 
                  command=self.show_help).pack(side=tk.LEFT, padx=2)
    
    def create_enhanced_control_panel(self, parent):
        """创建增强版控制面板"""
        control_frame = ttk.LabelFrame(parent, text="🎛️ 智能控制面板", padding="15")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        
        # 创建Notebook用于分组功能
        control_notebook = ttk.Notebook(control_frame)
        control_notebook.pack(fill=tk.BOTH, expand=True)
        
        # 智能选股标签页
        self.create_smart_screening_tab(control_notebook)
        
        # 个股分析标签页
        self.create_stock_analysis_tab(control_notebook)
        
        # 高级功能标签页
        self.create_advanced_features_tab(control_notebook)
    
    def create_smart_screening_tab(self, notebook):
        """创建智能选股标签页"""
        screening_frame = ttk.Frame(notebook, padding="10")
        notebook.add(screening_frame, text="🔍 智能选股")
        
        # 规则输入区域
        rule_frame = ttk.LabelFrame(screening_frame, text="自然语言规则输入", padding="10")
        rule_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 输入提示
        hint_label = ttk.Label(rule_frame, 
                              text="💡 支持复杂自然语言描述，如：'寻找市值超过200亿的大盘股，PE小于25倍'",
                              font=('Arial', 9), foreground='#7f8c8d')
        hint_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 规则输入文本框
        self.rule_text = scrolledtext.ScrolledText(rule_frame, height=4, width=50,
                                                  font=('Consolas', 10))
        self.rule_text.pack(fill=tk.X, pady=(0, 10))
        
        # 实时解析显示
        parse_frame = ttk.LabelFrame(rule_frame, text="实时解析结果", padding="5")
        parse_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.parse_result_text = tk.Text(parse_frame, height=3, width=50,
                                        font=('Consolas', 9), state=tk.DISABLED,
                                        bg='#f8f9fa', fg='#495057')
        self.parse_result_text.pack(fill=tk.X)
        
        # 绑定实时解析事件
        self.rule_text.bind('<KeyRelease>', self.on_rule_text_change)
        
        # 智能建议区域
        suggestion_frame = ttk.LabelFrame(screening_frame, text="智能建议", padding="10")
        suggestion_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 预设规则按钮（增强版）
        preset_rules = [
            ("🎯 价值投资", "寻找市值大于100亿的大盘股，PE小于20，PB小于2，涨幅大于2%"),
            ("⚡ 成长股", "筛选中小盘股票，PE在15到40之间，涨幅大于5%，成交量活跃"),
            ("🔥 热门概念", "新能源或科技股，涨幅大于3%，市值大于50亿"),
            ("💎 低估值", "股价小于20元，PB小于1.5，PE小于15的价值股"),
            ("🚀 突破股", "股价突破20日均线，涨幅大于5%，成交量大于平均水平")
        ]
        
        for i, (name, rule) in enumerate(preset_rules):
            btn = ttk.Button(suggestion_frame, text=name, width=15,
                           command=lambda r=rule: self.set_rule_text(r))
            btn.grid(row=i//2, column=i%2, padx=5, pady=2, sticky=tk.W)
        
        # 筛选参数
        param_frame = ttk.Frame(screening_frame)
        param_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(param_frame, text="最大结果数:").pack(side=tk.LEFT)
        self.limit_var = tk.StringVar(value="50")
        limit_entry = ttk.Entry(param_frame, textvariable=self.limit_var, width=10)
        limit_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(param_frame, text="置信度阈值:").pack(side=tk.LEFT)
        self.confidence_var = tk.StringVar(value="0.7")
        confidence_entry = ttk.Entry(param_frame, textvariable=self.confidence_var, width=10)
        confidence_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        # 筛选按钮
        button_frame = ttk.Frame(screening_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.screen_btn = ttk.Button(button_frame, text="🔍 开始智能筛选", 
                                   style='Primary.TButton',
                                   command=self.start_enhanced_screening)
        self.screen_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="📝 保存规则", 
                  command=self.save_rule).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🕒 历史规则", 
                  command=self.show_rule_history).pack(side=tk.LEFT)
    
    def create_stock_analysis_tab(self, notebook):
        """创建个股分析标签页"""
        analysis_frame = ttk.Frame(notebook, padding="10")
        notebook.add(analysis_frame, text="📊 个股分析")
        
        # 股票输入区域
        input_frame = ttk.LabelFrame(analysis_frame, text="股票信息", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 股票代码输入
        code_frame = ttk.Frame(input_frame)
        code_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(code_frame, text="股票代码:").pack(side=tk.LEFT)
        self.stock_code_var = tk.StringVar()
        code_entry = ttk.Entry(code_frame, textvariable=self.stock_code_var, width=15)
        code_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        # 智能搜索按钮
        ttk.Button(code_frame, text="🔍 智能搜索", 
                  command=self.smart_stock_search).pack(side=tk.LEFT, padx=(0, 10))
        
        # 分析参数
        param_frame = ttk.Frame(input_frame)
        param_frame.pack(fill=tk.X)
        
        ttk.Label(param_frame, text="分析天数:").pack(side=tk.LEFT)
        self.days_var = tk.StringVar(value="60")
        days_entry = ttk.Entry(param_frame, textvariable=self.days_var, width=10)
        days_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(param_frame, text="分析类型:").pack(side=tk.LEFT)
        self.analysis_type_var = tk.StringVar(value="综合分析")
        analysis_combo = ttk.Combobox(param_frame, textvariable=self.analysis_type_var,
                                    values=["综合分析", "技术分析", "基本面分析", "风险分析"],
                                    width=12, state="readonly")
        analysis_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # 分析按钮
        self.analyze_btn = ttk.Button(input_frame, text="📈 开始分析", 
                                    style='Success.TButton',
                                    command=self.start_enhanced_analysis)
        self.analyze_btn.pack(pady=(10, 0))
    
    def create_advanced_features_tab(self, notebook):
        """创建高级功能标签页"""
        advanced_frame = ttk.Frame(notebook, padding="10")
        notebook.add(advanced_frame, text="⚙️ 高级功能")
        
        # 批量分析
        batch_frame = ttk.LabelFrame(advanced_frame, text="批量分析", padding="10")
        batch_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(batch_frame, text="📁 导入股票列表", 
                  command=self.import_stock_list).pack(fill=tk.X, pady=2)
        ttk.Button(batch_frame, text="🔄 批量技术分析", 
                  command=self.batch_technical_analysis).pack(fill=tk.X, pady=2)
        ttk.Button(batch_frame, text="📊 生成对比报告", 
                  command=self.generate_comparison_report).pack(fill=tk.X, pady=2)
        
        # 数据管理
        data_frame = ttk.LabelFrame(advanced_frame, text="数据管理", padding="10")
        data_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(data_frame, text="🔄 更新数据源", 
                  command=self.update_data_sources).pack(fill=tk.X, pady=2)
        ttk.Button(data_frame, text="🧹 清理缓存", 
                  command=self.clear_cache).pack(fill=tk.X, pady=2)
        ttk.Button(data_frame, text="📋 数据源状态", 
                  command=self.show_data_source_status).pack(fill=tk.X, pady=2)
        
        # 系统设置
        settings_frame = ttk.LabelFrame(advanced_frame, text="系统设置", padding="10")
        settings_frame.pack(fill=tk.X)
        
        # 主题选择
        theme_frame = ttk.Frame(settings_frame)
        theme_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(theme_frame, text="界面主题:").pack(side=tk.LEFT)
        self.theme_var = tk.StringVar(value="默认")
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                 values=["默认", "深色", "护眼", "高对比度"],
                                 width=12, state="readonly")
        theme_combo.pack(side=tk.LEFT, padx=(5, 0))
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        # 其他设置
        ttk.Button(settings_frame, text="🔧 高级设置", 
                  command=self.show_advanced_settings).pack(fill=tk.X, pady=2)
    
    def create_enhanced_result_panel(self, parent):
        """创建增强版结果显示面板"""
        # 创建Notebook用于标签页
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          pady=(0, 15))
        
        # 筛选结果标签页（增强版）
        self.create_enhanced_screening_tab()
        
        # 个股分析标签页（增强版）
        self.create_enhanced_analysis_tab()
        
        # 技术图表标签页（增强版）
        self.create_enhanced_chart_tab()
        
        # 新增：对比分析标签页
        self.create_comparison_tab()
        
        # 新增：AI洞察标签页
        self.create_ai_insights_tab()
    
    def create_enhanced_screening_tab(self):
        """创建增强版筛选结果标签页"""
        screening_frame = ttk.Frame(self.notebook)
        self.notebook.add(screening_frame, text="📋 筛选结果")
        
        # 工具栏
        toolbar_frame = ttk.Frame(screening_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar_frame, text="📊 排序", 
                  command=self.sort_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="🔍 筛选", 
                  command=self.filter_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="📈 添加到对比", 
                  command=self.add_to_comparison).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="💾 导出结果", 
                  command=self.export_results).pack(side=tk.RIGHT)
        
        # 结果统计
        stats_frame = ttk.Frame(screening_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="等待筛选...", 
                                    font=('Arial', 10), foreground='#7f8c8d')
        self.stats_label.pack(side=tk.LEFT)
        
        # 结果表格（增强版）
        columns = ('代码', '名称', '现价', '涨跌幅', '成交量', '市值(亿)', 'PE', 'PB', '置信度', '匹配度')
        self.result_tree = ttk.Treeview(screening_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题和宽度
        column_widths = {'代码': 80, '名称': 100, '现价': 80, '涨跌幅': 80, 
                        '成交量': 100, '市值(亿)': 100, 'PE': 60, 'PB': 60, 
                        '置信度': 80, '匹配度': 80}
        
        for col in columns:
            self.result_tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.result_tree.column(col, width=column_widths.get(col, 80), anchor=tk.CENTER)
        
        # 绑定双击事件
        self.result_tree.bind('<Double-1>', self.on_stock_double_click)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(screening_frame, orient=tk.VERTICAL, 
                                   command=self.result_tree.yview)
        scrollbar_x = ttk.Scrollbar(screening_frame, orient=tk.HORIZONTAL, 
                                   command=self.result_tree.xview)
        self.result_tree.configure(yscrollcommand=scrollbar_y.set, 
                                  xscrollcommand=scrollbar_x.set)
        
        # 布局
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右键菜单
        self.result_tree.bind('<Button-3>', self.show_context_menu)
    
    def create_enhanced_analysis_tab(self):
        """创建增强版个股分析标签页"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="📊 个股分析")
        
        # 创建PanedWindow用于分割显示
        paned_window = ttk.PanedWindow(analysis_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：分析报告
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="📋 分析报告", style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        self.analysis_text = scrolledtext.ScrolledText(left_frame, 
                                                      font=('Consolas', 10),
                                                      wrap=tk.WORD)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
        
        # 右侧：关键指标
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)
        
        ttk.Label(right_frame, text="📈 关键指标", style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        # 指标显示区域
        self.indicators_frame = ttk.Frame(right_frame)
        self.indicators_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_enhanced_chart_tab(self):
        """创建增强版技术图表标签页"""
        chart_frame = ttk.Frame(self.notebook)
        self.notebook.add(chart_frame, text="📈 技术图表")
        
        # 图表工具栏
        chart_toolbar = ttk.Frame(chart_frame)
        chart_toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(chart_toolbar, text="图表类型:").pack(side=tk.LEFT)
        self.chart_type_var = tk.StringVar(value="K线图")
        chart_combo = ttk.Combobox(chart_toolbar, textvariable=self.chart_type_var,
                                 values=["K线图", "分时图", "技术指标", "对比图"],
                                 width=10, state="readonly")
        chart_combo.pack(side=tk.LEFT, padx=(5, 15))
        chart_combo.bind('<<ComboboxSelected>>', self.change_chart_type)
        
        ttk.Button(chart_toolbar, text="🔄 刷新", 
                  command=self.refresh_chart).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(chart_toolbar, text="💾 保存图表", 
                  command=self.save_chart).pack(side=tk.LEFT, padx=(0, 5))
        
        # 创建matplotlib图表
        self.fig = Figure(figsize=(14, 10), dpi=100, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 图表工具栏
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(self.canvas, chart_frame)
        toolbar.update()
    
    def create_comparison_tab(self):
        """创建对比分析标签页"""
        comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(comparison_frame, text="⚖️ 对比分析")
        
        # 对比股票选择
        selection_frame = ttk.LabelFrame(comparison_frame, text="选择对比股票", padding="10")
        selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.comparison_listbox = tk.Listbox(selection_frame, height=4, selectmode=tk.MULTIPLE)
        self.comparison_listbox.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = ttk.Frame(selection_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="➕ 添加股票", 
                  command=self.add_comparison_stock).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="➖ 移除股票", 
                  command=self.remove_comparison_stock).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="📊 开始对比", 
                  command=self.start_comparison).pack(side=tk.RIGHT)
        
        # 对比结果显示
        self.comparison_result = scrolledtext.ScrolledText(comparison_frame, 
                                                          font=('Consolas', 10))
        self.comparison_result.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
    
    def create_ai_insights_tab(self):
        """创建AI洞察标签页"""
        insights_frame = ttk.Frame(self.notebook)
        self.notebook.add(insights_frame, text="🤖 AI洞察")
        
        # AI分析控制
        control_frame = ttk.LabelFrame(insights_frame, text="AI分析控制", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(control_frame, text="🧠 生成市场洞察", 
                  command=self.generate_market_insights).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="🎯 个股AI评分", 
                  command=self.generate_ai_score).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="📈 趋势预测", 
                  command=self.predict_trend).pack(side=tk.LEFT)
        
        # AI洞察结果
        self.insights_text = scrolledtext.ScrolledText(insights_frame, 
                                                      font=('Arial', 11),
                                                      wrap=tk.WORD)
        self.insights_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
    
    def create_enhanced_status_bar(self, parent):
        """创建增强版状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        
        # 主状态信息
        self.status_var = tk.StringVar()
        self.status_var.set("🚀 正在初始化增强版分析器...")
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          length=200, mode='determinate')
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 数据源状态指示器
        self.data_status_label = ttk.Label(status_frame, text="📡 数据源: 检查中...", 
                                          font=('Arial', 9))
        self.data_status_label.pack(side=tk.RIGHT, padx=(10, 10))
    
    def init_analyzer(self):
        """初始化分析器"""
        def init_thread():
            try:
                self.status_var.set("🔄 正在初始化数据接口...")
                self.progress_var.set(25)
                
                self.analyzer = StockAnalyzer()
                self.progress_var.set(75)
                
                self.status_var.set("✅ 系统就绪 - 增强版功能已启用")
                self.progress_var.set(100)
                
                self.data_status_label.configure(text="📡 数据源: 正常", 
                                                style='Success.TLabel')
                
                # 启用按钮
                self.screen_btn.configure(state=tk.NORMAL)
                self.analyze_btn.configure(state=tk.NORMAL)
                
            except Exception as e:
                self.status_var.set(f"❌ 初始化失败: {str(e)}")
                self.data_status_label.configure(text="📡 数据源: 异常", 
                                                style='Error.TLabel')
                messagebox.showerror("错误", f"系统初始化失败:\n{str(e)}")
        
        thread = threading.Thread(target=init_thread, daemon=True)
        thread.start()
    
    # 事件处理方法
    def on_rule_text_change(self, event=None):
        """规则文本变化时的实时解析"""
        rule_text = self.rule_text.get(1.0, tk.END).strip()
        if not rule_text:
            self.update_parse_result("请输入筛选规则...")
            return
        
        try:
            result = self.enhanced_parser.parse_rule(rule_text)
            
            parse_info = f"解析结果: {len(result['conditions'])}个条件 | "
            parse_info += f"逻辑: {result['logic']} | "
            parse_info += f"置信度: {result['confidence']:.2f}\n"
            
            for i, condition in enumerate(result['conditions'], 1):
                parse_info += f"{i}. {condition['description']}\n"
            
            self.update_parse_result(parse_info)
            
        except Exception as e:
            self.update_parse_result(f"解析错误: {str(e)}")
    
    def update_parse_result(self, text):
        """更新解析结果显示"""
        self.parse_result_text.configure(state=tk.NORMAL)
        self.parse_result_text.delete(1.0, tk.END)
        self.parse_result_text.insert(1.0, text)
        self.parse_result_text.configure(state=tk.DISABLED)
    
    def set_rule_text(self, rule):
        """设置规则文本"""
        self.rule_text.delete(1.0, tk.END)
        self.rule_text.insert(1.0, rule)
        self.on_rule_text_change()
    
    def start_enhanced_screening(self):
        """开始增强版筛选"""
        if not self.analyzer:
            messagebox.showwarning("警告", "分析器尚未初始化完成")
            return
        
        rule_text = self.rule_text.get(1.0, tk.END).strip()
        if not rule_text:
            messagebox.showwarning("警告", "请输入筛选规则")
            return
        
        try:
            limit = int(self.limit_var.get())
            confidence_threshold = float(self.confidence_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return
        
        # 在后台线程中执行筛选
        def screening_thread():
            try:
                self.status_var.set("🔍 正在进行智能筛选...")
                self.screen_btn.configure(state=tk.DISABLED)
                self.progress_var.set(0)
                
                # 使用增强版解析器
                parsed_result = self.enhanced_parser.parse_rule(rule_text)
                self.progress_var.set(25)
                
                if parsed_result['confidence'] < confidence_threshold:
                    self.root.after(0, lambda: messagebox.showwarning(
                        "警告", f"规则解析置信度({parsed_result['confidence']:.2f})低于阈值({confidence_threshold})，建议调整规则表达"))
                
                # 执行筛选
                stocks = self.analyzer.screen_stocks_by_rule(rule_text, limit)
                self.progress_var.set(75)
                
                # 保存到历史记录
                self.rule_history.append({
                    'rule': rule_text,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'result_count': len(stocks),
                    'confidence': parsed_result['confidence']
                })
                
                # 在主线程中更新UI
                self.root.after(0, self.update_enhanced_screening_results, stocks, parsed_result)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"筛选失败:\n{str(e)}"))
            finally:
                self.root.after(0, lambda: self.screen_btn.configure(state=tk.NORMAL))
                self.root.after(0, lambda: self.progress_var.set(100))
                self.root.after(0, lambda: self.status_var.set("✅ 筛选完成"))
        
        thread = threading.Thread(target=screening_thread, daemon=True)
        thread.start()
    
    def update_enhanced_screening_results(self, stocks: List[StockData], parsed_result: Dict):
        """更新增强版筛选结果"""
        # 清空现有结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        # 添加新结果
        self.current_stocks = stocks
        for stock in stocks:
            market_cap_yi = stock.market_cap / 100000000 if stock.market_cap > 0 else 0
            volume_wan = stock.volume / 10000 if stock.volume > 0 else 0
            
            # 计算匹配度（简化版）
            match_score = min(95, 70 + len(parsed_result['conditions']) * 5)
            
            self.result_tree.insert('', tk.END, values=(
                stock.symbol,
                stock.name,
                f"{stock.current_price:.2f}",
                f"{stock.change_pct:.2f}%",
                f"{volume_wan:.0f}万",
                f"{market_cap_yi:.2f}",
                f"{stock.pe_ratio:.2f}" if stock.pe_ratio > 0 else "--",
                f"{stock.pb_ratio:.2f}" if stock.pb_ratio > 0 else "--",
                f"{parsed_result['confidence']:.2f}",
                f"{match_score}%"
            ))
        
        # 更新统计信息
        stats_text = f"📊 找到 {len(stocks)} 只符合条件的股票 | "
        stats_text += f"解析置信度: {parsed_result['confidence']:.2f} | "
        stats_text += f"条件数: {len(parsed_result['conditions'])}"
        self.stats_label.configure(text=stats_text)
        
        # 切换到筛选结果标签页
        self.notebook.select(0)
    
    # 其他功能方法（简化实现）
    def save_config(self):
        """保存配置"""
        config = {
            'theme': self.theme_var.get(),
            'rule_history': self.rule_history[-10:],  # 保存最近10条
            'settings': {
                'confidence_threshold': self.confidence_var.get(),
                'default_limit': self.limit_var.get()
            }
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("配置文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", "配置已保存")
            except Exception as e:
                messagebox.showerror("错误", f"保存配置失败:\n{str(e)}")
    
    def load_config(self):
        """加载配置"""
        filename = filedialog.askopenfilename(
            filetypes=[("配置文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 应用配置
                if 'theme' in config:
                    self.theme_var.set(config['theme'])
                
                if 'rule_history' in config:
                    self.rule_history.extend(config['rule_history'])
                
                if 'settings' in config:
                    settings = config['settings']
                    if 'confidence_threshold' in settings:
                        self.confidence_var.set(settings['confidence_threshold'])
                    if 'default_limit' in settings:
                        self.limit_var.set(settings['default_limit'])
                
                messagebox.showinfo("成功", "配置已加载")
                
            except Exception as e:
                messagebox.showerror("错误", f"加载配置失败:\n{str(e)}")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🚀 智能股票分析系统 - 增强版 v2.0

🔍 智能选股功能:
• 支持复杂自然语言描述
• 实时解析显示
• 智能建议和预设规则
• 置信度评估

📊 个股分析功能:
• 综合技术分析
• 基本面分析
• 风险评估
• AI评分系统

⚖️ 对比分析功能:
• 多股票对比
• 指标对比图表
• 相关性分析

🤖 AI洞察功能:
• 市场趋势分析
• 个股AI评分
• 智能推荐

💡 使用技巧:
• 使用自然语言描述选股条件
• 关注解析置信度
• 利用预设规则快速开始
• 保存常用配置

📞 技术支持:
如有问题，请查看系统日志或联系技术支持。
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("帮助信息")
        help_window.geometry("600x500")
        
        help_text_widget = scrolledtext.ScrolledText(help_window, 
                                                    font=('Arial', 11),
                                                    wrap=tk.WORD)
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.configure(state=tk.DISABLED)
    
    # 简化的其他方法实现
    def save_rule(self):
        messagebox.showinfo("提示", "规则已保存到历史记录")
    
    def show_rule_history(self):
        if not self.rule_history:
            messagebox.showinfo("提示", "暂无历史规则")
            return
        
        history_text = "\n".join([f"{h['timestamp']}: {h['rule']} (结果:{h['result_count']}只)" 
                                 for h in self.rule_history[-10:]])
        messagebox.showinfo("历史规则", history_text)
    
    def start_enhanced_analysis(self):
        messagebox.showinfo("提示", "增强版个股分析功能开发中...")
    
    def smart_stock_search(self):
        messagebox.showinfo("提示", "智能股票搜索功能开发中...")
    
    def change_theme(self, event=None):
        messagebox.showinfo("提示", f"主题切换功能开发中，当前选择: {self.theme_var.get()}")
    
    def show_advanced_settings(self):
        messagebox.showinfo("提示", "高级设置功能开发中...")
    
    # 技术图表功能实现
    def update_stock_chart(self, stock_data):
        """更新股票技术图表"""
        if not stock_data or stock_data.historical_data.empty:
            return
        
        # 清空现有图表
        self.fig.clear()
        
        # 准备数据
        hist_data = stock_data.historical_data.copy()
        # BaoStock返回的字段名是英文的
        if 'date' in hist_data.columns:
            hist_data['date'] = pd.to_datetime(hist_data['date'])
            hist_data.set_index('date', inplace=True)
        elif '日期' in hist_data.columns:
            hist_data['日期'] = pd.to_datetime(hist_data['日期'])
            hist_data.set_index('日期', inplace=True)
        
        # 获取收盘价数据
        if 'close' in hist_data.columns:
            close_prices = pd.to_numeric(hist_data['close'], errors='coerce')
        elif '收盘' in hist_data.columns:
            close_prices = pd.to_numeric(hist_data['收盘'], errors='coerce')
        else:
            close_prices = pd.Series()
        
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
        self.notebook.select(1)  # 技术图表是第2个标签页
    
    def on_stock_double_click(self, event):
        """双击股票列表项时的处理"""
        selection = self.result_tree.selection()
        if selection:
            item = self.result_tree.item(selection[0])
            stock_code = str(item['values'][0])  # 确保股票代码为字符串类型
            
            # 开始个股分析并显示图表
            self.analyze_single_stock(stock_code)
    
    def analyze_single_stock(self, stock_code):
        """分析单只股票并显示图表"""
        if not self.analyzer:
            messagebox.showwarning("警告", "分析器尚未初始化完成")
            return
        
        def analysis_thread():
            try:
                self.status_var.set(f"🔍 正在分析股票 {stock_code}...")
                self.progress_var.set(0)
                
                # 获取股票数据
                stock_data = self.analyzer.analyze_stock(stock_code, days=60)
                self.progress_var.set(50)
                
                if stock_data:
                    # 在主线程中更新UI
                    self.root.after(0, self.update_stock_chart, stock_data)
                    self.root.after(0, self.update_analysis_text, stock_data)
                    self.root.after(0, lambda: self.status_var.set(f"✅ {stock_data.name} 分析完成"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("错误", f"无法获取股票 {stock_code} 的数据"))
                    
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: messagebox.showerror("错误", f"分析失败:\n{error_msg}"))
            finally:
                self.root.after(0, lambda: self.progress_var.set(100))
        
        thread = threading.Thread(target=analysis_thread, daemon=True)
        thread.start()
    
    def update_analysis_text(self, stock_data):
        """更新分析文本"""
        if not stock_data:
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, "无法获取股票数据")
            return
        
        # 生成分析报告
        report = self.generate_stock_report(stock_data)
        
        # 更新文本显示
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, report)
    
    def generate_stock_report(self, stock_data) -> str:
        """生成股票分析报告"""
        report = f"\n=== {stock_data.name}({stock_data.symbol}) 分析报告 ===\n"
        
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
                
                report += f"  MACD: {macd_current:.4f}\n"
                report += f"  Signal: {signal_current:.4f}\n"
                
                if macd_current > signal_current:
                    report += "  ✓ MACD金叉信号\n"
                else:
                    report += "  ✗ MACD死叉信号\n"
        
        # 历史数据统计
        if not stock_data.historical_data.empty:
            hist_data = stock_data.historical_data
            
            # 获取收盘价数据，兼容中英文字段名
            if 'close' in hist_data.columns:
                close_prices = pd.to_numeric(hist_data['close'], errors='coerce')
            elif '收盘' in hist_data.columns:
                close_prices = pd.to_numeric(hist_data['收盘'], errors='coerce')
            else:
                close_prices = pd.Series()
            
            if not close_prices.empty and not close_prices.isna().all():
                report += "\n历史数据统计:\n"
                report += f"  数据天数: {len(hist_data)} 天\n"
                report += f"  最高价: {close_prices.max():.2f} 元\n"
                report += f"  最低价: {close_prices.min():.2f} 元\n"
                report += f"  平均价: {close_prices.mean():.2f} 元\n"
                report += f"  价格波动率: {close_prices.std():.2f}\n"
            else:
                report += "\n历史数据统计:\n"
                report += "  暂无有效的价格数据\n"
        
        return report
    
    def export_results(self):
        """导出筛选结果"""
        if not hasattr(self, 'current_stocks') or not self.current_stocks:
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
    
    # 图表控制方法
    def change_chart_type(self, event):
        """切换图表类型"""
        chart_type = self.chart_type_var.get()
        messagebox.showinfo("提示", f"图表类型切换功能开发中，当前选择: {chart_type}")
    
    def refresh_chart(self):
        """刷新图表"""
        messagebox.showinfo("提示", "请双击股票列表中的股票来显示图表")
    
    def save_chart(self):
        """保存图表"""
        if hasattr(self, 'fig'):
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG文件", "*.png"), ("PDF文件", "*.pdf"), ("所有文件", "*.*")]
            )
            if filename:
                try:
                    self.fig.savefig(filename, dpi=300, bbox_inches='tight')
                    messagebox.showinfo("成功", f"图表已保存到:\n{filename}")
                except Exception as e:
                    messagebox.showerror("错误", f"保存失败:\n{str(e)}")
        else:
            messagebox.showwarning("警告", "没有可保存的图表")
    
    # 其他占位方法
    def sort_results(self): pass
    def filter_results(self): pass
    def add_to_comparison(self): pass
    def sort_by_column(self, col): pass
    def show_context_menu(self, event): pass
    
    def add_comparison_stock(self):
        """添加股票到对比分析"""
        if not self.analyzer:
            messagebox.showwarning("警告", "分析器尚未初始化完成")
            return
        
        # 弹出对话框让用户输入股票代码
        dialog = tk.Toplevel(self.root)
        dialog.title("添加对比股票")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # 输入框
        ttk.Label(dialog, text="请输入股票代码（如：000001）:", font=('Arial', 11)).pack(pady=20)
        
        entry_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=entry_var, font=('Arial', 12), width=20)
        entry.pack(pady=10)
        entry.focus()
        
        # 按钮框架
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def add_stock():
            stock_code = entry_var.get().strip()
            if not stock_code:
                messagebox.showwarning("警告", "请输入股票代码")
                return
            
            # 标准化股票代码格式
            if not stock_code.startswith(('sh.', 'sz.')):
                if stock_code.startswith('6'):
                    stock_code = f'sh.{stock_code}'
                elif stock_code.startswith(('0', '3')):
                    stock_code = f'sz.{stock_code}'
                else:
                    messagebox.showerror("错误", "无效的股票代码格式")
                    return
            
            # 检查是否已存在
            existing_items = [self.comparison_listbox.get(i) for i in range(self.comparison_listbox.size())]
            for item in existing_items:
                if stock_code in item:
                    messagebox.showwarning("警告", "该股票已在对比列表中")
                    return
            
            # 获取股票信息并添加到列表
            try:
                self.status_var.set(f"正在获取股票 {stock_code} 信息...")
                stock_data = self.analyzer.analyze_stock(stock_code, days=30)
                
                if stock_data:
                    display_text = f"{stock_data.symbol} - {stock_data.name} (¥{stock_data.current_price:.2f})"
                    self.comparison_listbox.insert(tk.END, display_text)
                    self.status_var.set(f"✅ 已添加股票: {stock_data.name}")
                    dialog.destroy()
                else:
                    messagebox.showerror("错误", f"无法获取股票 {stock_code} 的信息")
                    self.status_var.set("❌ 添加股票失败")
            except Exception as e:
                messagebox.showerror("错误", f"添加股票失败:\n{str(e)}")
                self.status_var.set("❌ 添加股票失败")
        
        def cancel():
            dialog.destroy()
        
        # 绑定回车键
        entry.bind('<Return>', lambda e: add_stock())
        
        ttk.Button(button_frame, text="添加", command=add_stock).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=cancel).pack(side=tk.LEFT)
    
    def remove_comparison_stock(self):
        """移除对比股票"""
        selection = self.comparison_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要移除的股票")
            return
        
        # 获取选中的股票信息
        selected_items = [self.comparison_listbox.get(i) for i in selection]
        
        # 确认删除
        if len(selected_items) == 1:
            confirm_msg = f"确定要移除股票 {selected_items[0]} 吗？"
        else:
            confirm_msg = f"确定要移除选中的 {len(selected_items)} 只股票吗？"
        
        if messagebox.askyesno("确认", confirm_msg):
            # 从后往前删除，避免索引变化
            for i in reversed(selection):
                self.comparison_listbox.delete(i)
            
            self.status_var.set(f"✅ 已移除 {len(selected_items)} 只股票")
    def start_comparison(self):
        """开始股票对比分析"""
        if self.comparison_listbox.size() < 2:
            messagebox.showwarning("警告", "请至少添加2只股票进行对比")
            return
        
        if not self.analyzer:
            messagebox.showwarning("警告", "分析器尚未初始化完成")
            return
        
        # 获取所有对比股票的代码
        stock_codes = []
        for i in range(self.comparison_listbox.size()):
            item_text = self.comparison_listbox.get(i)
            # 提取股票代码（格式：sh.000001 - 平安银行 (¥12.34)）
            code = item_text.split(' - ')[0]
            stock_codes.append(code)
        
        # 在后台线程中执行对比分析
        def comparison_thread():
            try:
                self.status_var.set("🔍 正在进行股票对比分析...")
                self.progress_var.set(0)
                
                # 获取所有股票数据
                stock_data_list = []
                for i, code in enumerate(stock_codes):
                    self.status_var.set(f"正在分析股票 {code}...")
                    self.progress_var.set((i + 1) * 80 / len(stock_codes))
                    
                    stock_data = self.analyzer.analyze_stock(code, days=30)
                    if stock_data:
                        stock_data_list.append(stock_data)
                    else:
                        print(f"警告：无法获取股票 {code} 的数据")
                
                if len(stock_data_list) < 2:
                    self.root.after(0, lambda: messagebox.showerror("错误", "获取股票数据失败，无法进行对比"))
                    return
                
                # 生成对比报告
                self.progress_var.set(90)
                report = self.generate_comparison_report_content(stock_data_list)
                
                # 在主线程中更新UI
                self.root.after(0, self.update_comparison_results, report)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"对比分析失败:\n{str(e)}"))
            finally:
                self.root.after(0, lambda: self.progress_var.set(100))
                self.root.after(0, lambda: self.status_var.set("✅ 对比分析完成"))
        
        thread = threading.Thread(target=comparison_thread, daemon=True)
        thread.start()
    
    def generate_comparison_report_content(self, stock_data_list) -> str:
        """生成股票对比报告内容"""
        report = "\n" + "=" * 60 + "\n"
        report += f"📊 股票对比分析报告 ({len(stock_data_list)}只股票)\n"
        report += "=" * 60 + "\n\n"
        
        # 基本信息对比表
        report += "📋 基本信息对比:\n"
        report += "-" * 80 + "\n"
        report += f"{'股票代码':<12} {'股票名称':<12} {'现价':<8} {'涨跌幅%':<8} {'市值(亿)':<10} {'PE':<6} {'PB':<6}\n"
        report += "-" * 80 + "\n"
        
        for stock in stock_data_list:
            market_cap_yi = stock.market_cap / 100000000 if stock.market_cap > 0 else 0
            pe_str = f"{stock.pe_ratio:.1f}" if stock.pe_ratio > 0 else "--"
            pb_str = f"{stock.pb_ratio:.1f}" if stock.pb_ratio > 0 else "--"
            
            report += f"{stock.symbol:<12} {stock.name[:10]:<12} {stock.current_price:<8.2f} "
            report += f"{stock.change_pct:<8.2f} {market_cap_yi:<10.1f} {pe_str:<6} {pb_str:<6}\n"
        
        # 技术指标对比
        report += "\n📈 技术指标对比:\n"
        report += "-" * 80 + "\n"
        
        for stock in stock_data_list:
            report += f"\n🔸 {stock.name}({stock.symbol}):\n"
            
            if stock.technical_indicators:
                # MA分析
                if 'ma5' in stock.technical_indicators and 'ma20' in stock.technical_indicators:
                    ma5 = stock.technical_indicators['ma5'].iloc[-1]
                    ma20 = stock.technical_indicators['ma20'].iloc[-1]
                    report += f"  MA5: {ma5:.2f}  MA20: {ma20:.2f}\n"
                    
                    if stock.current_price > ma5 and stock.current_price > ma20:
                        report += "  ✅ 多头排列\n"
                    elif stock.current_price < ma5 and stock.current_price < ma20:
                        report += "  ❌ 空头排列\n"
                    else:
                        report += "  ⚠️ 震荡整理\n"
                
                # RSI分析
                if 'rsi' in stock.technical_indicators:
                    rsi = stock.technical_indicators['rsi'].iloc[-1]
                    report += f"  RSI: {rsi:.1f}"
                    if rsi > 70:
                        report += " (超买)\n"
                    elif rsi < 30:
                        report += " (超卖)\n"
                    else:
                        report += " (正常)\n"
            else:
                report += "  暂无技术指标数据\n"
        
        # 投资建议
        report += "\n💡 投资建议:\n"
        report += "-" * 40 + "\n"
        
        # 按涨跌幅排序
        sorted_stocks = sorted(stock_data_list, key=lambda x: x.change_pct, reverse=True)
        
        report += f"📈 今日表现最佳: {sorted_stocks[0].name} (+{sorted_stocks[0].change_pct:.2f}%)\n"
        report += f"📉 今日表现最差: {sorted_stocks[-1].name} ({sorted_stocks[-1].change_pct:+.2f}%)\n\n"
        
        # 估值对比
        valid_pe_stocks = [s for s in stock_data_list if s.pe_ratio > 0]
        if valid_pe_stocks:
            min_pe_stock = min(valid_pe_stocks, key=lambda x: x.pe_ratio)
            report += f"💰 估值最低(PE): {min_pe_stock.name} (PE: {min_pe_stock.pe_ratio:.1f})\n"
        
        # 市值对比
        if all(s.market_cap > 0 for s in stock_data_list):
            max_cap_stock = max(stock_data_list, key=lambda x: x.market_cap)
            min_cap_stock = min(stock_data_list, key=lambda x: x.market_cap)
            report += f"🏢 市值最大: {max_cap_stock.name} ({max_cap_stock.market_cap/100000000:.1f}亿)\n"
            report += f"🏪 市值最小: {min_cap_stock.name} ({min_cap_stock.market_cap/100000000:.1f}亿)\n"
        
        report += "\n" + "=" * 60 + "\n"
        report += f"📅 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "⚠️  以上分析仅供参考，投资有风险，入市需谨慎！\n"
        report += "=" * 60 + "\n"
        
        return report
    
    def update_comparison_results(self, report):
        """更新对比分析结果显示"""
        self.comparison_result.delete(1.0, tk.END)
        self.comparison_result.insert(tk.END, report)
        
        # 滚动到顶部
        self.comparison_result.see(1.0)
    def generate_market_insights(self): pass
    def generate_ai_score(self): pass
    def predict_trend(self): pass
    def import_stock_list(self): pass
    def batch_technical_analysis(self): pass
    def generate_comparison_report(self): pass
    def update_data_sources(self): pass
    def clear_cache(self): pass
    def show_data_source_status(self): pass

def main():
    """主函数"""
    root = tk.Tk()
    app = EnhancedStockGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()