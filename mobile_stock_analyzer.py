#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端股票分析器
专为Android应用优化的轻量级股票分析模块
不依赖pandas/numpy，仅使用Python标准库
"""

from datetime import datetime, timedelta
import re
import json
import random
import statistics

# 完全移除baostock依赖，使用纯Python模拟数据
HAS_BAOSTOCK = False
print("使用纯Python模拟数据模式，避免C扩展编译问题")

class MobileStockData:
    """移动端股票数据结构（简化版）"""
    def __init__(self, symbol, name, current_price, change_pct, volume, market_cap, pe_ratio, pb_ratio):
        self.symbol = symbol
        self.name = name
        self.current_price = current_price
        self.change_pct = change_pct
        self.volume = volume
        self.market_cap = market_cap
        self.pe_ratio = pe_ratio
        self.pb_ratio = pb_ratio
    
class MobileNLPParser:
    """移动端自然语言解析器（轻量级）"""
    
    def __init__(self):
        self.rule_patterns = {
            # 价格相关
            'price_gt': r'(?:股价|价格)(?:大于|超过|高于)([\d.]+)(?:元)?',
            'price_lt': r'(?:股价|价格)(?:小于|低于|少于)([\d.]+)(?:元)?',
            'price_range': r'(?:股价|价格)(?:在|介于)([\d.]+)(?:元)?(?:到|至|-)([\d.]+)(?:元)?',
            
            # 涨跌幅相关
            'change_gt': r'(?:涨幅|涨跌幅)(?:大于|超过|高于)([\d.]+)%?',
            'change_lt': r'(?:涨幅|涨跌幅)(?:小于|低于|少于)([\d.]+)%?',
            
            # 市值相关
            'market_cap_gt': r'(?:市值)(?:大于|超过|高于)([\d.]+)(?:亿|万亿)?',
            'market_cap_lt': r'(?:市值)(?:小于|低于|少于)([\d.]+)(?:亿|万亿)?',
            
            # PE/PB相关
            'pe_lt': r'PE(?:比率)?(?:小于|低于|少于)([\d.]+)(?:倍)?',
            'pe_gt': r'PE(?:比率)?(?:大于|超过|高于)([\d.]+)(?:倍)?',
            'pb_lt': r'PB(?:比率)?(?:小于|低于|少于)([\d.]+)(?:倍)?',
            'pb_gt': r'PB(?:比率)?(?:大于|超过|高于)([\d.]+)(?:倍)?',
            
            # 成交量相关
            'volume_gt': r'(?:成交量)(?:大于|超过|高于)([\d.]+)(?:万手|手|万)?',
        }
    
    def parse_rule(self, rule_text):
        """解析自然语言规则"""
        conditions = []
        confidence = 0.8
        
        for pattern_name, pattern in self.rule_patterns.items():
            matches = re.findall(pattern, rule_text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    conditions.append({
                        'type': pattern_name,
                        'values': match
                    })
                else:
                    conditions.append({
                        'type': pattern_name,
                        'value': float(match)
                    })
        
        return {
            'conditions': conditions,
            'confidence': confidence,
            'original_text': rule_text
        }

class MobileDataProvider:
    """移动端数据提供者"""
    
    def __init__(self):
        self.logged_in = False
        if HAS_BAOSTOCK:
            self._login()
        else:
            print("使用模拟数据模式")
    
    def _login(self):
        """登录BaoStock"""
        try:
            lg = bs.login()
            if lg.error_code == '0':
                self.logged_in = True
                print("BaoStock登录成功")
            else:
                print(f"BaoStock登录失败: {lg.error_msg}")
        except Exception as e:
            print(f"BaoStock登录异常: {e}")
    
    def get_stock_list(self):
        """获取股票列表（简化版）"""
        if not HAS_BAOSTOCK or not self.logged_in:
            return self._get_mock_stock_list()
        
        try:
            # 获取最近交易日的股票列表
            for days_back in range(10):
                query_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
                
                rs = bs.query_all_stock(day=query_date)
                if rs.error_code != '0':
                    continue
                
                stock_list = []
                count = 0
                while rs.next() and count < 100:  # 限制数量以提高性能
                    row = rs.get_row_data()
                    if row[1] and row[2]:  # 确保有股票代码和名称
                        stock_list.append({
                            '代码': row[1].split('.')[-1],  # 去掉前缀
                            '名称': row[2],
                            '现价': round(random.uniform(5, 50), 2),  # 模拟价格
                            '涨跌幅': round(random.uniform(-10, 10), 2),
                            '成交量': int(random.uniform(1000, 100000)),
                            '市值(亿)': round(random.uniform(10, 1000), 2),
                            'PE': round(random.uniform(5, 50), 2),
                            'PB': round(random.uniform(0.5, 5), 2)
                        })
                        count += 1
                
                if stock_list:
                    return stock_list
            
            return self._get_mock_stock_list()
            
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            return self._get_mock_stock_list()
    
    def _get_mock_stock_list(self):
        """获取模拟股票数据"""
        mock_stocks = [
            {'代码': '000001', '名称': '平安银行', '现价': 12.50, '涨跌幅': 2.1, '成交量': 50000, '市值(亿)': 2400, 'PE': 6.5, 'PB': 0.8},
            {'代码': '000002', '名称': '万科A', '现价': 18.30, '涨跌幅': -1.2, '成交量': 80000, '市值(亿)': 2000, 'PE': 8.2, 'PB': 1.1},
            {'代码': '000858', '名称': '五粮液', '现价': 168.50, '涨跌幅': 3.5, '成交量': 30000, '市值(亿)': 6500, 'PE': 25.3, 'PB': 4.2},
            {'代码': '600036', '名称': '招商银行', '现价': 35.80, '涨跌幅': 1.8, '成交量': 45000, '市值(亿)': 9200, 'PE': 7.8, 'PB': 1.2},
            {'代码': '600519', '名称': '贵州茅台', '现价': 1680.00, '涨跌幅': -0.5, '成交量': 15000, '市值(亿)': 21000, 'PE': 28.5, 'PB': 12.8},
            {'代码': '600887', '名称': '伊利股份', '现价': 32.40, '涨跌幅': 2.8, '成交量': 35000, '市值(亿)': 2100, 'PE': 18.6, 'PB': 3.5},
            {'代码': '000858', '名称': '五粮液', '现价': 168.50, '涨跌幅': 3.5, '成交量': 30000, '市值(亿)': 6500, 'PE': 25.3, 'PB': 4.2},
            {'代码': '002415', '名称': '海康威视', '现价': 28.90, '涨跌幅': 4.2, '成交量': 60000, '市值(亿)': 2700, 'PE': 15.2, 'PB': 2.8},
            {'代码': '300059', '名称': '东方财富', '现价': 15.60, '涨跌幅': 6.8, '成交量': 120000, '市值(亿)': 2400, 'PE': 22.1, 'PB': 3.2},
            {'代码': '002594', '名称': '比亚迪', '现价': 245.80, '涨跌幅': 5.5, '成交量': 40000, '市值(亿)': 7100, 'PE': 35.6, 'PB': 6.8}
        ]
        
        # 添加一些随机变化
        for stock in mock_stocks:
            stock['现价'] *= random.uniform(0.95, 1.05)
            stock['涨跌幅'] += random.uniform(-1, 1)
            stock['成交量'] = int(stock['成交量'] * random.uniform(0.8, 1.2))
            
            # 四舍五入
            stock['现价'] = round(stock['现价'], 2)
            stock['涨跌幅'] = round(stock['涨跌幅'], 2)
        
        return mock_stocks
    
    def get_stock_info(self, code):
        """获取单个股票信息"""
        stock_list = self.get_stock_list()
        
        for stock in stock_list:
            if stock['代码'] == code:
                return MobileStockData(
                    symbol=stock['代码'],
                    name=stock['名称'],
                    current_price=stock['现价'],
                    change_pct=stock['涨跌幅'],
                    volume=stock['成交量'],
                    market_cap=stock['市值(亿)'] * 100000000,  # 转换为元
                    pe_ratio=stock['PE'],
                    pb_ratio=stock['PB']
                )
        
        return None

class MobileStockAnalyzer:
    """移动端股票分析器主类"""
    
    def __init__(self):
        self.data_provider = MobileDataProvider()
        self.nlp_parser = MobileNLPParser()
        self.initialized = True
        print("移动端股票分析器初始化完成")
    
    def screen_stocks_by_rule(self, rule_text, limit=50):
        """根据规则筛选股票"""
        try:
            # 解析规则
            parsed_rule = self.nlp_parser.parse_rule(rule_text)
            conditions = parsed_rule['conditions']
            
            # 获取股票列表
            all_stocks = self.data_provider.get_stock_list()
            
            # 应用筛选条件
            filtered_stocks = []
            for stock in all_stocks:
                if self._match_conditions(stock, conditions):
                    filtered_stocks.append(stock)
                
                if len(filtered_stocks) >= limit:
                    break
            
            return filtered_stocks[:limit]
            
        except Exception as e:
            print(f"筛选股票失败: {e}")
            return []
    
    def _match_conditions(self, stock, conditions):
        """检查股票是否匹配条件"""
        for condition in conditions:
            condition_type = condition['type']
            
            try:
                if condition_type == 'price_gt':
                    if stock['现价'] <= condition['value']:
                        return False
                elif condition_type == 'price_lt':
                    if stock['现价'] >= condition['value']:
                        return False
                elif condition_type == 'change_gt':
                    if stock['涨跌幅'] <= condition['value']:
                        return False
                elif condition_type == 'change_lt':
                    if stock['涨跌幅'] >= condition['value']:
                        return False
                elif condition_type == 'market_cap_gt':
                    if stock['市值(亿)'] <= condition['value']:
                        return False
                elif condition_type == 'market_cap_lt':
                    if stock['市值(亿)'] >= condition['value']:
                        return False
                elif condition_type == 'pe_lt':
                    if stock['PE'] >= condition['value']:
                        return False
                elif condition_type == 'pe_gt':
                    if stock['PE'] <= condition['value']:
                        return False
                elif condition_type == 'pb_lt':
                    if stock['PB'] >= condition['value']:
                        return False
                elif condition_type == 'pb_gt':
                    if stock['PB'] <= condition['value']:
                        return False
                elif condition_type == 'volume_gt':
                    if stock['成交量'] <= condition['value'] * 10000:  # 转换为手
                        return False
            except (KeyError, ValueError, TypeError):
                continue
        
        return True
    
    def analyze_stock(self, code, days=60):
        """分析单个股票"""
        try:
            return self.data_provider.get_stock_info(code)
        except Exception as e:
            print(f"分析股票 {code} 失败: {e}")
            return None
    
    def get_market_summary(self):
        """获取市场概况"""
        try:
            stocks = self.data_provider.get_stock_list()
            if not stocks:
                return {}
            
            # 计算市场统计
            prices = [s['现价'] for s in stocks]
            changes = [s['涨跌幅'] for s in stocks]
            
            return {
                'total_stocks': len(stocks),
                'avg_price': round(statistics.mean(prices), 2),
                'avg_change': round(statistics.mean(changes), 2),
                'rising_count': len([c for c in changes if c > 0]),
                'falling_count': len([c for c in changes if c < 0]),
                'flat_count': len([c for c in changes if c == 0])
            }
        except Exception as e:
            print(f"获取市场概况失败: {e}")
            return {}

# 为了兼容性，创建别名
StockAnalyzer = MobileStockAnalyzer

if __name__ == '__main__':
    # 测试代码
    analyzer = MobileStockAnalyzer()
    
    # 测试筛选功能
    print("测试筛选功能...")
    results = analyzer.screen_stocks_by_rule("股价大于20元且涨幅大于2%", 5)
    print(f"筛选结果: {len(results)} 只股票")
    for stock in results:
        print(f"  {stock['名称']}({stock['代码']}): {stock['现价']}元, {stock['涨跌幅']}%")
    
    # 测试个股分析
    print("\n测试个股分析...")
    stock_info = analyzer.analyze_stock('000001')
    if stock_info:
        print(f"股票信息: {stock_info.name}({stock_info.symbol})")
        print(f"当前价格: {stock_info.current_price}元")
        print(f"涨跌幅: {stock_info.change_pct}%")
    
    # 测试市场概况
    print("\n测试市场概况...")
    summary = analyzer.get_market_summary()
    print(f"市场概况: {summary}")