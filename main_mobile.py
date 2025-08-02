#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能股票分析系统 - 移动端版本
使用Kivy框架构建Android应用
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import platform
import threading
import asyncio
from datetime import datetime

# 导入核心分析模块
try:
    from mobile_stock_analyzer import MobileStockAnalyzer as StockAnalyzer
except ImportError:
    # 如果导入失败，创建简化版本
    class StockAnalyzer:
        def __init__(self):
            self.initialized = False
        
        def screen_stocks_by_rule(self, rule, limit=50):
            return []
        
        def analyze_stock(self, code, days=60):
            return None

class StockCard(BoxLayout):
    """股票信息卡片组件"""
    
    def __init__(self, stock_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = dp(10)
        self.spacing = dp(5)
        
        # 创建卡片内容
        self.create_card_content(stock_data)
    
    def create_card_content(self, stock_data):
        """创建卡片内容"""
        # 股票名称和代码
        header = BoxLayout(orientation='horizontal', size_hint_y=0.4)
        name_label = Label(
            text=f"{stock_data.get('名称', 'N/A')} ({stock_data.get('代码', 'N/A')})",
            font_size=dp(16),
            bold=True,
            text_size=(None, None),
            halign='left'
        )
        header.add_widget(name_label)
        self.add_widget(header)
        
        # 价格信息
        price_layout = GridLayout(cols=2, size_hint_y=0.6)
        
        # 左列：价格和涨跌幅
        left_col = BoxLayout(orientation='vertical')
        price_label = Label(
            text=f"价格: {stock_data.get('现价', 'N/A')}",
            font_size=dp(14)
        )
        change_label = Label(
            text=f"涨跌: {stock_data.get('涨跌幅', 'N/A')}%",
            font_size=dp(14)
        )
        left_col.add_widget(price_label)
        left_col.add_widget(change_label)
        
        # 右列：成交量和市值
        right_col = BoxLayout(orientation='vertical')
        volume_label = Label(
            text=f"成交量: {stock_data.get('成交量', 'N/A')}",
            font_size=dp(12)
        )
        market_cap_label = Label(
            text=f"市值: {stock_data.get('市值(亿)', 'N/A')}亿",
            font_size=dp(12)
        )
        right_col.add_widget(volume_label)
        right_col.add_widget(market_cap_label)
        
        price_layout.add_widget(left_col)
        price_layout.add_widget(right_col)
        self.add_widget(price_layout)

class ScreeningTab(TabbedPanelItem):
    """选股标签页"""
    
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.text = '智能选股'
        self.app_instance = app_instance
        self.create_content()
    
    def create_content(self):
        """创建选股界面内容"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 标题
        title = Label(
            text='🔍 智能选股系统',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(40),
            bold=True
        )
        main_layout.add_widget(title)
        
        # 规则输入区域
        rule_label = Label(
            text='请输入选股规则（支持自然语言）:',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30),
            text_size=(None, None),
            halign='left'
        )
        main_layout.add_widget(rule_label)
        
        # 规则输入框
        self.rule_input = TextInput(
            multiline=True,
            size_hint_y=None,
            height=dp(100),
            hint_text='例如：股价大于10元且涨幅大于3%',
            font_size=dp(14)
        )
        main_layout.add_widget(self.rule_input)
        
        # 快速选择按钮
        quick_buttons_layout = GridLayout(cols=2, size_hint_y=None, height=dp(120), spacing=dp(5))
        
        preset_rules = [
            ("价值投资", "市值大于100亿且PE小于20"),
            ("成长股", "涨幅大于5%且成交量活跃"),
            ("热门概念", "新能源或科技股，涨幅大于3%"),
            ("低估值", "PB小于1.5且PE小于15")
        ]
        
        for name, rule in preset_rules:
            btn = Button(
                text=name,
                size_hint_y=None,
                height=dp(50),
                font_size=dp(12)
            )
            btn.bind(on_press=lambda x, r=rule: self.set_rule(r))
            quick_buttons_layout.add_widget(btn)
        
        main_layout.add_widget(quick_buttons_layout)
        
        # 参数设置
        param_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        param_layout.add_widget(Label(text='最大结果数:', size_hint_x=0.3))
        self.limit_input = TextInput(
            text='50',
            size_hint_x=0.2,
            multiline=False,
            input_filter='int'
        )
        param_layout.add_widget(self.limit_input)
        main_layout.add_widget(param_layout)
        
        # 筛选按钮
        self.screen_button = Button(
            text='🚀 开始筛选',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16),
            bold=True
        )
        self.screen_button.bind(on_press=self.start_screening)
        main_layout.add_widget(self.screen_button)
        
        # 进度条
        self.progress_bar = ProgressBar(
            size_hint_y=None,
            height=dp(20),
            opacity=0
        )
        main_layout.add_widget(self.progress_bar)
        
        # 结果显示区域
        self.results_scroll = ScrollView()
        self.results_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        self.results_scroll.add_widget(self.results_layout)
        main_layout.add_widget(self.results_scroll)
        
        self.add_widget(main_layout)
    
    def set_rule(self, rule):
        """设置预设规则"""
        self.rule_input.text = rule
    
    def start_screening(self, instance):
        """开始筛选股票"""
        rule = self.rule_input.text.strip()
        if not rule:
            self.show_popup("错误", "请输入选股规则")
            return
        
        limit = int(self.limit_input.text) if self.limit_input.text.isdigit() else 50
        
        # 显示进度条
        self.progress_bar.opacity = 1
        self.screen_button.disabled = True
        self.screen_button.text = "筛选中..."
        
        # 在后台线程中执行筛选
        threading.Thread(target=self.perform_screening, args=(rule, limit)).start()
    
    def perform_screening(self, rule, limit):
        """执行筛选（后台线程）"""
        try:
            # 模拟筛选过程
            import time
            time.sleep(2)  # 模拟网络请求
            
            # 这里应该调用实际的筛选逻辑
            results = self.app_instance.analyzer.screen_stocks_by_rule(rule, limit)
            
            # 在主线程中更新UI
            Clock.schedule_once(lambda dt: self.update_results(results), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(str(e)), 0)
    
    def update_results(self, results):
        """更新筛选结果"""
        # 清空之前的结果
        self.results_layout.clear_widgets()
        
        if not results:
            no_result_label = Label(
                text='未找到符合条件的股票',
                size_hint_y=None,
                height=dp(50)
            )
            self.results_layout.add_widget(no_result_label)
        else:
            # 添加结果标题
            result_title = Label(
                text=f'找到 {len(results)} 只股票:',
                size_hint_y=None,
                height=dp(40),
                font_size=dp(16),
                bold=True
            )
            self.results_layout.add_widget(result_title)
            
            # 添加股票卡片
            for stock in results:
                card = StockCard(stock)
                self.results_layout.add_widget(card)
        
        # 隐藏进度条，恢复按钮
        self.progress_bar.opacity = 0
        self.screen_button.disabled = False
        self.screen_button.text = "🚀 开始筛选"
    
    def show_error(self, error_msg):
        """显示错误信息"""
        self.progress_bar.opacity = 0
        self.screen_button.disabled = False
        self.screen_button.text = "🚀 开始筛选"
        self.show_popup("错误", f"筛选失败: {error_msg}")
    
    def show_popup(self, title, message):
        """显示弹窗"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class AnalysisTab(TabbedPanelItem):
    """个股分析标签页"""
    
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.text = '个股分析'
        self.app_instance = app_instance
        self.create_content()
    
    def create_content(self):
        """创建个股分析界面"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 标题
        title = Label(
            text='📊 个股分析',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(40),
            bold=True
        )
        main_layout.add_widget(title)
        
        # 股票代码输入
        code_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        code_layout.add_widget(Label(text='股票代码:', size_hint_x=0.3))
        self.code_input = TextInput(
            hint_text='例如: 000001',
            size_hint_x=0.5,
            multiline=False
        )
        code_layout.add_widget(self.code_input)
        
        analyze_btn = Button(
            text='分析',
            size_hint_x=0.2
        )
        analyze_btn.bind(on_press=self.start_analysis)
        code_layout.add_widget(analyze_btn)
        
        main_layout.add_widget(code_layout)
        
        # 分析结果显示区域
        self.analysis_scroll = ScrollView()
        self.analysis_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.analysis_layout.bind(minimum_height=self.analysis_layout.setter('height'))
        self.analysis_scroll.add_widget(self.analysis_layout)
        main_layout.add_widget(self.analysis_scroll)
        
        self.add_widget(main_layout)
    
    def start_analysis(self, instance):
        """开始分析股票"""
        code = self.code_input.text.strip()
        if not code:
            self.show_popup("错误", "请输入股票代码")
            return
        
        # 在后台线程中执行分析
        threading.Thread(target=self.perform_analysis, args=(code,)).start()
    
    def perform_analysis(self, code):
        """执行股票分析"""
        try:
            # 模拟分析过程
            import time
            time.sleep(1)
            
            # 这里应该调用实际的分析逻辑
            result = self.app_instance.analyzer.analyze_stock(code)
            
            # 在主线程中更新UI
            Clock.schedule_once(lambda dt: self.update_analysis_result(result), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_popup("错误", f"分析失败: {str(e)}"), 0)
    
    def update_analysis_result(self, result):
        """更新分析结果"""
        # 清空之前的结果
        self.analysis_layout.clear_widgets()
        
        if not result:
            no_result_label = Label(
                text='无法获取股票数据',
                size_hint_y=None,
                height=dp(50)
            )
            self.analysis_layout.add_widget(no_result_label)
        else:
            # 显示分析结果
            result_text = f"""
股票名称: {getattr(result, 'name', 'N/A')}
股票代码: {getattr(result, 'symbol', 'N/A')}
当前价格: {getattr(result, 'current_price', 'N/A')} 元
涨跌幅: {getattr(result, 'change_pct', 'N/A')}%
市值: {getattr(result, 'market_cap', 0)/100000000:.2f} 亿元
PE比率: {getattr(result, 'pe_ratio', 'N/A')}
PB比率: {getattr(result, 'pb_ratio', 'N/A')}
            """
            
            result_label = Label(
                text=result_text,
                size_hint_y=None,
                height=dp(200),
                text_size=(None, None),
                halign='left',
                valign='top'
            )
            self.analysis_layout.add_widget(result_label)
    
    def show_popup(self, title, message):
        """显示弹窗"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class StockAnalysisApp(App):
    """股票分析应用主类"""
    
    def build(self):
        """构建应用界面"""
        # 初始化分析器
        self.analyzer = StockAnalyzer()
        
        # 创建主界面
        root = BoxLayout(orientation='vertical')
        
        # 标题栏
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=dp(10)
        )
        
        title_label = Label(
            text='🚀 智能股票分析',
            font_size=dp(18),
            bold=True
        )
        header.add_widget(title_label)
        
        root.add_widget(header)
        
        # 创建标签页面板
        tab_panel = TabbedPanel()
        tab_panel.do_default_tab = False
        
        # 添加选股标签页
        screening_tab = ScreeningTab(self)
        tab_panel.add_widget(screening_tab)
        
        # 添加个股分析标签页
        analysis_tab = AnalysisTab(self)
        tab_panel.add_widget(analysis_tab)
        
        root.add_widget(tab_panel)
        
        return root
    
    def on_start(self):
        """应用启动时的初始化"""
        print("股票分析应用启动成功")
    
    def on_stop(self):
        """应用停止时的清理"""
        print("股票分析应用已停止")

if __name__ == '__main__':
    StockAnalysisApp().run()