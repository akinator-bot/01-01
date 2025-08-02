#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版自然语言解析器
突破当前系统的限制，支持更复杂的自然语言描述
"""

import re
from typing import Dict, List, Tuple, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ParsedCondition:
    """解析后的条件"""
    field: str
    operator: str
    value: Any
    confidence: float = 1.0
    description: str = ""

class EnhancedNLPParser:
    """增强版自然语言解析器"""
    
    def __init__(self):
        # 初始化jieba分词
        self._init_jieba()
        
        # 字段映射词典
        self.field_synonyms = {
            'price': ['股价', '价格', '收盘价', '现价', '最新价', '股票价格'],
            'change_pct': ['涨幅', '涨跌幅', '涨幅度', '涨跌', '涨跌率', '变动幅度'],
            'volume': ['成交量', '交易量', '成交额', '交易额', '成交手数'],
            'market_cap': ['市值', '总市值', '流通市值', '市场价值'],
            'pe_ratio': ['PE', '市盈率', '动态市盈率', '静态市盈率'],
            'pb_ratio': ['PB', '市净率', '账面价值比'],
            'turnover_rate': ['换手率', '流通率'],
            'rsi': ['RSI', '相对强弱指数', '强弱指标'],
            'ma': ['均线', '移动平均线', 'MA', '平均线']
        }
        
        # 操作符映射
        self.operator_synonyms = {
            '>': ['大于', '高于', '超过', '多于', '超越', '高出', '>', '＞'],
            '<': ['小于', '低于', '少于', '不足', '低过', '<', '＜'],
            '>=': ['大于等于', '不少于', '至少', '不低于', '>=', '≥'],
            '<=': ['小于等于', '不超过', '至多', '不高于', '<=', '≤'],
            '=': ['等于', '是', '为', '=', '＝'],
            'between': ['之间', '介于', '在...之间', '从...到', '范围']
        }
        
        # 数值单位转换
        self.unit_multipliers = {
            '万': 10000,
            '十万': 100000,
            '百万': 1000000,
            '千万': 10000000,
            '亿': 100000000,
            '十亿': 1000000000,
            '百亿': 10000000000,
            '千亿': 100000000000,
            '万亿': 1000000000000
        }
        
        # 模糊概念映射
        self.fuzzy_concepts = {
            '大盘股': {'field': 'market_cap', 'operator': '>', 'value': 50000000000},  # 500亿以上
            '中盘股': {'field': 'market_cap', 'operator': 'between', 'value': [10000000000, 50000000000]},
            '小盘股': {'field': 'market_cap', 'operator': '<', 'value': 10000000000},  # 100亿以下
            '高价股': {'field': 'current_price', 'operator': '>', 'value': 50},
            '中价股': {'field': 'current_price', 'operator': 'between', 'value': [10, 50]},
            '低价股': {'field': 'current_price', 'operator': '<', 'value': 10},
            '活跃股': {'field': 'turnover_rate', 'operator': '>', 'value': 5},
            '不错的': {'field': 'change_pct', 'operator': '>', 'value': 2},
            '表现好': {'field': 'change_pct', 'operator': '>', 'value': 3},
            '有潜力': {'field': 'pe_ratio', 'operator': '<', 'value': 30},
            '价值股': {'field': 'pb_ratio', 'operator': '<', 'value': 2},
            '成长股': {'field': 'pe_ratio', 'operator': 'between', 'value': [15, 40]}
        }
        
        # 行业概念词典（简化版）
        self.industry_concepts = {
            '新能源': ['新能源', '电动车', '锂电池', '光伏', '风电', '储能'],
            '科技股': ['科技', '互联网', '人工智能', 'AI', '芯片', '半导体'],
            '医药股': ['医药', '生物医药', '疫苗', '医疗器械', '中药'],
            '金融股': ['银行', '保险', '证券', '信托', '基金'],
            '地产股': ['房地产', '建筑', '装修', '物业'],
            '消费股': ['白酒', '食品', '零售', '服装', '家电']
        }
        
        # 否定词
        self.negation_words = ['不', '不要', '避免', '排除', '非', '无', '没有']
        
        # 逻辑连接词
        self.logic_connectors = {
            'AND': ['且', '和', '并且', '同时', '以及', '&', '&&'],
            'OR': ['或', '或者', '要么', '|', '||']
        }
    
    def _init_jieba(self):
        """初始化分词器（简化版）"""
        # 股票相关词汇列表（用于后续处理）
        self.stock_words = [
            '股价', '涨幅', '市值', '市盈率', '市净率', '成交量', '换手率',
            'RSI', 'MACD', '均线', '大盘股', '小盘股', '新能源', '科技股'
        ]
    
    def parse_rule(self, rule_text: str) -> Dict:
        """解析自然语言规则"""
        print(f"\n🔍 开始解析规则: {rule_text}")
        
        # 预处理
        processed_text = self._preprocess_text(rule_text)
        print(f"📝 预处理后: {processed_text}")
        
        # 分词和词性标注
        words = self._segment_text(processed_text)
        print(f"🔤 分词结果: {words}")
        
        # 识别逻辑关系
        logic_type = self._detect_logic(processed_text)
        print(f"🔗 逻辑关系: {logic_type}")
        
        # 提取条件
        conditions = self._extract_conditions(processed_text, words)
        print(f"📊 提取条件: {len(conditions)}个")
        
        # 处理模糊概念
        fuzzy_conditions = self._handle_fuzzy_concepts(processed_text)
        conditions.extend(fuzzy_conditions)
        
        # 处理行业概念
        industry_conditions = self._handle_industry_concepts(processed_text)
        conditions.extend(industry_conditions)
        
        return {
            'original_text': rule_text,
            'processed_text': processed_text,
            'conditions': [self._condition_to_dict(c) for c in conditions],
            'logic': logic_type,
            'confidence': self._calculate_confidence(conditions)
        }
    
    def _preprocess_text(self, text: str) -> str:
        """文本预处理"""
        # 统一标点符号
        text = text.replace('，', ',')
        text = text.replace('。', '.')
        text = text.replace('；', ';')
        text = text.replace('：', ':')
        
        # 处理数字表达
        text = self._normalize_numbers(text)
        
        # 处理否定表达
        text = self._handle_negations(text)
        
        return text.strip()
    
    def _normalize_numbers(self, text: str) -> str:
        """标准化数字表达"""
        # 中文数字转阿拉伯数字
        chinese_numbers = {
            '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
            '六': '6', '七': '7', '八': '8', '九': '9', '十': '10',
            '百': '100', '千': '1000'
        }
        
        for cn, num in chinese_numbers.items():
            text = text.replace(cn, num)
        
        # 处理复合数字表达
        patterns = [
            (r'(\d+)十(\d+)', lambda m: str(int(m.group(1)) * 10 + int(m.group(2)))),
            (r'(\d+)百(\d+)十(\d+)', lambda m: str(int(m.group(1)) * 100 + int(m.group(2)) * 10 + int(m.group(3)))),
        ]
        
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def _handle_negations(self, text: str) -> str:
        """处理否定表达"""
        # 简单的否定处理，将"不要太高"转换为"小于某个值"
        negation_patterns = [
            (r'不要太高', '小于50'),
            (r'不要太低', '大于5'),
            (r'避免高价', '小于30'),
            (r'排除低价', '大于10')
        ]
        
        for pattern, replacement in negation_patterns:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def _segment_text(self, text: str) -> List[Tuple[str, str]]:
        """简单分词和词性标注"""
        # 使用正则表达式进行简单分词
        tokens = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+|\d+(?:\.\d+)?|[><=≥≤]', text)
        # 简单的词性标注（这里简化处理）
        result = []
        for token in tokens:
            if re.match(r'\d+(?:\.\d+)?', token):
                result.append((token, 'm'))  # 数词
            elif token in ['>', '<', '>=', '<=', '=', '≥', '≤']:
                result.append((token, 'p'))  # 介词
            else:
                result.append((token, 'n'))  # 名词
        return result
    
    def _detect_logic(self, text: str) -> str:
        """检测逻辑关系"""
        # 检查OR逻辑
        for connector in self.logic_connectors['OR']:
            if connector in text:
                return 'OR'
        
        # 默认AND逻辑
        return 'AND'
    
    def _extract_conditions(self, text: str, words: List[Tuple[str, str]]) -> List[ParsedCondition]:
        """提取条件"""
        conditions = []
        
        # 使用改进的正则表达式模式
        patterns = self._get_enhanced_patterns()
        
        for pattern_name, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                condition = self._create_condition_from_match(pattern_name, match)
                if condition:
                    conditions.append(condition)
        
        return conditions
    
    def _get_enhanced_patterns(self) -> Dict[str, str]:
        """获取增强的正则表达式模式"""
        return {
            # 价格相关 - 支持更多表达方式
            'price_above': r'(?:股价|价格|收盘价|现价|最新价)(?:要|需要|应该)?(?:大于|高于|超过|多于|>|＞)\s*(\d+(?:\.\d+)?)(?:元|块)?',
            'price_below': r'(?:股价|价格|收盘价|现价|最新价)(?:要|需要|应该)?(?:小于|低于|少于|不足|<|＜)\s*(\d+(?:\.\d+)?)(?:元|块)?',
            'price_range': r'(?:股价|价格|收盘价)(?:在|介于|从)\s*(\d+(?:\.\d+)?)(?:元|块)?(?:到|至|-|~)\s*(\d+(?:\.\d+)?)(?:元|块)?(?:之间|范围)?',
            
            # 涨跌幅相关 - 支持更多表达
            'change_above': r'(?:涨幅|涨跌幅|涨幅度|涨跌|上涨)(?:要|需要|应该)?(?:大于|高于|超过|多于|>|＞)\s*(\d+(?:\.\d+)?)(?:%|个百分点|百分点)?',
            'change_positive': r'(?:上涨|涨|正涨幅|涨幅为正)',
            
            # 市值相关 - 支持中文数字
            'market_cap_above': r'(?:市值|总市值)(?:要|需要|应该)?(?:大于|高于|超过|多于|>|＞)\s*(\d+(?:\.\d+)?)(?:万|十万|百万|千万|亿|十亿|百亿|千亿|万亿)?(?:元)?',
            'market_cap_below': r'(?:市值|总市值)(?:要|需要|应该)?(?:小于|低于|少于|不足|<|＜)\s*(\d+(?:\.\d+)?)(?:万|十万|百万|千万|亿|十亿|百亿|千亿|万亿)?(?:元)?',
            
            # PE/PB相关
            'pe_below': r'(?:PE|市盈率|动态市盈率)(?:要|需要|应该)?(?:小于|低于|少于|不足|<|＜)\s*(\d+(?:\.\d+)?)(?:倍)?',
            'pb_below': r'(?:PB|市净率)(?:要|需要|应该)?(?:小于|低于|少于|不足|<|＜)\s*(\d+(?:\.\d+)?)(?:倍)?',
            
            # 成交量相关
            'volume_above': r'(?:成交量|交易量)(?:要|需要|应该)?(?:大于|高于|超过|多于|>|＞)\s*(\d+(?:\.\d+)?)(?:万|千万|亿)?(?:手|股)?',
            
            # 复合条件
            'comprehensive_condition': r'(?:寻找|找|选择|筛选)(?:一些)?(.+?)(?:股票|股|的股票)',
        }
    
    def _create_condition_from_match(self, pattern_name: str, match) -> ParsedCondition:
        """从匹配结果创建条件"""
        try:
            if pattern_name == 'price_above':
                return ParsedCondition(
                    field='current_price',
                    operator='>',
                    value=float(match.group(1)),
                    description=f"股价大于{match.group(1)}元"
                )
            elif pattern_name == 'price_below':
                return ParsedCondition(
                    field='current_price',
                    operator='<',
                    value=float(match.group(1)),
                    description=f"股价小于{match.group(1)}元"
                )
            elif pattern_name == 'price_range':
                return ParsedCondition(
                    field='current_price',
                    operator='between',
                    value=[float(match.group(1)), float(match.group(2))],
                    description=f"股价在{match.group(1)}-{match.group(2)}元之间"
                )
            elif pattern_name == 'change_above':
                return ParsedCondition(
                    field='change_pct',
                    operator='>',
                    value=float(match.group(1)),
                    description=f"涨幅大于{match.group(1)}%"
                )
            elif pattern_name == 'change_positive':
                return ParsedCondition(
                    field='change_pct',
                    operator='>',
                    value=0,
                    description="涨幅为正"
                )
            elif pattern_name == 'market_cap_above':
                value = float(match.group(1))
                # 处理单位
                unit_text = match.group(0)
                multiplier = self._get_unit_multiplier(unit_text)
                return ParsedCondition(
                    field='market_cap',
                    operator='>',
                    value=value * multiplier,
                    description=f"市值大于{match.group(1)}{self._extract_unit(unit_text)}"
                )
            elif pattern_name == 'pe_below':
                return ParsedCondition(
                    field='pe_ratio',
                    operator='<',
                    value=float(match.group(1)),
                    description=f"PE小于{match.group(1)}"
                )
            elif pattern_name == 'pb_below':
                return ParsedCondition(
                    field='pb_ratio',
                    operator='<',
                    value=float(match.group(1)),
                    description=f"PB小于{match.group(1)}"
                )
            # 可以继续添加更多条件类型
            
        except (ValueError, IndexError) as e:
            print(f"⚠️ 创建条件失败: {e}")
            return None
        
        return None
    
    def _get_unit_multiplier(self, text: str) -> float:
        """获取单位乘数"""
        for unit, multiplier in self.unit_multipliers.items():
            if unit in text:
                return multiplier
        return 1.0
    
    def _extract_unit(self, text: str) -> str:
        """提取单位"""
        for unit in self.unit_multipliers.keys():
            if unit in text:
                return unit
        return ""
    
    def _handle_fuzzy_concepts(self, text: str) -> List[ParsedCondition]:
        """处理模糊概念"""
        conditions = []
        
        for concept, condition_def in self.fuzzy_concepts.items():
            if concept in text:
                condition = ParsedCondition(
                    field=condition_def['field'],
                    operator=condition_def['operator'],
                    value=condition_def['value'],
                    confidence=0.8,  # 模糊概念置信度较低
                    description=f"模糊概念: {concept}"
                )
                conditions.append(condition)
        
        return conditions
    
    def _handle_industry_concepts(self, text: str) -> List[ParsedCondition]:
        """处理行业概念"""
        conditions = []
        
        for industry, keywords in self.industry_concepts.items():
            for keyword in keywords:
                if keyword in text:
                    # 行业概念转换为特定条件（这里简化处理）
                    condition = ParsedCondition(
                        field='industry',
                        operator='=',
                        value=industry,
                        confidence=0.9,
                        description=f"行业概念: {industry}"
                    )
                    conditions.append(condition)
                    break
        
        return conditions
    
    def _condition_to_dict(self, condition: ParsedCondition) -> Dict:
        """将条件对象转换为字典"""
        return {
            'field': condition.field,
            'operator': condition.operator,
            'value': condition.value,
            'confidence': condition.confidence,
            'description': condition.description
        }
    
    def _calculate_confidence(self, conditions: List[ParsedCondition]) -> float:
        """计算整体置信度"""
        if not conditions:
            return 0.0
        
        total_confidence = sum(c.confidence for c in conditions)
        return total_confidence / len(conditions)

# 测试函数
def test_enhanced_parser():
    """测试增强版解析器"""
    parser = EnhancedNLPParser()
    
    test_cases = [
        "寻找市值超过200亿元的大盘股，要求市盈率低于25倍，市净率小于2倍",
        "筛选股价高于20元但低于100元的中价股，涨幅要超过3个百分点",
        "找一些不错的股票，价格不要太高，涨得还可以",
        "帮我选择一些有潜力的中小盘股票，最好是最近表现不错的",
        "新能源概念股票，要求涨幅大于5%且成交量活跃",
        "股价在15到50元之间或者市值大于100亿的股票"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试用例 {i}: {test_case}")
        print('='*60)
        
        result = parser.parse_rule(test_case)
        
        print(f"\n✅ 解析结果:")
        print(f"📝 原始文本: {result['original_text']}")
        print(f"🔄 处理后文本: {result['processed_text']}")
        print(f"🔗 逻辑关系: {result['logic']}")
        print(f"📊 置信度: {result['confidence']:.2f}")
        print(f"🎯 识别条件数: {len(result['conditions'])}")
        
        for j, condition in enumerate(result['conditions'], 1):
            print(f"   {j}. {condition['description']} (置信度: {condition['confidence']:.2f})")

if __name__ == "__main__":
    test_enhanced_parser()