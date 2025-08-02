#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简化的Android测试应用
用于验证基本的Kivy构建是否正常
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class SimpleStockApp(App):
    """简化的股票应用"""
    
    def build(self):
        """构建应用界面"""
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 标题
        title = Label(
            text='简化股票分析应用',
            size_hint_y=None,
            height=60,
            font_size=24
        )
        main_layout.add_widget(title)
        
        # 输入框
        self.stock_input = TextInput(
            hint_text='输入股票代码（如：000001）',
            size_hint_y=None,
            height=40,
            multiline=False
        )
        main_layout.add_widget(self.stock_input)
        
        # 查询按钮
        query_btn = Button(
            text='查询股票',
            size_hint_y=None,
            height=50
        )
        query_btn.bind(on_press=self.query_stock)
        main_layout.add_widget(query_btn)
        
        # 结果显示
        self.result_label = Label(
            text='请输入股票代码进行查询',
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        main_layout.add_widget(self.result_label)
        
        return main_layout
    
    def query_stock(self, instance):
        """查询股票信息"""
        code = self.stock_input.text.strip()
        
        if not code:
            self.result_label.text = '请输入股票代码'
            return
        
        # 模拟股票数据
        mock_data = {
            '000001': {'name': '平安银行', 'price': 12.50, 'change': 2.1},
            '000002': {'name': '万科A', 'price': 18.30, 'change': -1.2},
            '600036': {'name': '招商银行', 'price': 35.80, 'change': 1.8},
            '600519': {'name': '贵州茅台', 'price': 1680.00, 'change': -0.5}
        }
        
        if code in mock_data:
            stock = mock_data[code]
            result_text = f"股票代码: {code}\n"
            result_text += f"股票名称: {stock['name']}\n"
            result_text += f"当前价格: {stock['price']}元\n"
            result_text += f"涨跌幅: {stock['change']}%"
            
            self.result_label.text = result_text
        else:
            self.result_label.text = f'未找到股票代码: {code}\n请尝试: 000001, 000002, 600036, 600519'

if __name__ == '__main__':
    SimpleStockApp().run()