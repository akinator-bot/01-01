#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析Web应用版本
作为Android APK的备选方案
"""

from flask import Flask, render_template, request, jsonify
import json
from mobile_stock_analyzer import MobileStockAnalyzer

app = Flask(__name__)
analyzer = MobileStockAnalyzer()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    """获取股票列表API"""
    try:
        stocks = analyzer.data_provider.get_stock_list()
        return jsonify({
            'success': True,
            'data': stocks
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/screen', methods=['POST'])
def screen_stocks():
    """股票筛选API"""
    try:
        data = request.get_json()
        rule = data.get('rule', '')
        limit = data.get('limit', 20)
        
        results = analyzer.screen_stocks_by_rule(rule, limit)
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/analyze/<code>')
def analyze_stock(code):
    """个股分析API"""
    try:
        result = analyzer.analyze_stock(code)
        
        if result:
            return jsonify({
                'success': True,
                'data': {
                    'symbol': result.symbol,
                    'name': result.name,
                    'current_price': result.current_price,
                    'change_pct': result.change_pct,
                    'volume': result.volume,
                    'market_cap': result.market_cap,
                    'pe_ratio': result.pe_ratio,
                    'pb_ratio': result.pb_ratio
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': '未找到股票信息'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/market')
def market_summary():
    """市场概况API"""
    try:
        summary = analyzer.get_market_summary()
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("启动股票分析Web应用...")
    print("访问地址: http://localhost:5000")
    print("按Ctrl+C停止服务")
    app.run(debug=True, host='0.0.0.0', port=5000)