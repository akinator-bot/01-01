# 🏆 智能股票分析系统

一个基于AI的股票分析和选股系统，支持自然语言规则输入，整合多个数据源，提供丰富的技术分析功能。

## ✨ 主要特性

### 🤖 AI驱动的自然语言选股
- 支持中文自然语言输入选股规则
- 智能解析用户描述，转换为可执行的筛选条件
- 支持复杂的组合条件和逻辑运算

### 📊 多数据源整合
- **AKShare**: 实时行情数据，数据丰富，接口简单
- **BaoStock**: 历史数据稳定，适合量化分析
- 自动数据源切换和容错处理

### 📈 丰富的技术分析
- 移动平均线（MA5, MA10, MA20）
- 相对强弱指数（RSI）
- MACD指标
- 布林带（Bollinger Bands）
- KDJ指标
- 自定义技术指标扩展

### 🖥️ 用户友好的界面
- 直观的图形界面（GUI）
- 命令行界面（CLI）支持
- 实时数据更新和图表展示
- 数据导出功能（Excel/CSV）

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Windows/macOS/Linux
- 网络连接（用于获取股票数据）

### 安装步骤

1. **克隆或下载项目**
```bash
git clone <项目地址>
cd 股票数据
```

2. **安装依赖包**
```bash
pip install -r requirements.txt
```

3. **运行系统**
```bash
# GUI模式（推荐）
python main.py

# 命令行模式
python main.py --cli

# 演示模式
python main.py --demo
```

## 📖 使用指南

### GUI界面使用

1. **启动系统**
   ```bash
   python main.py
   ```

2. **智能选股**
   - 在"控制面板"的"智能选股"区域输入自然语言规则
   - 点击"开始筛选"按钮
   - 在"筛选结果"标签页查看结果

3. **个股分析**
   - 在"个股分析"区域输入股票代码
   - 设置分析天数
   - 点击"分析"按钮
   - 查看"个股分析"和"技术图表"标签页

4. **数据导出**
   - 筛选完成后，点击"导出筛选结果"按钮
   - 选择保存格式（Excel/CSV）

### 命令行使用

```bash
python main.py --cli
```

按照提示选择功能：
- 选择1：智能选股
- 选择2：个股分析
- 选择3：退出

## 🎯 选股规则示例

### 基础规则
```
股价大于10元
涨幅大于5%
市值大于100亿
PE小于20
RSI在30到70之间
```

### 组合规则
```
股价大于10元且涨幅大于3%
市值大于50亿且PE小于30
RSI在30到70之间且股价站上20日均线
涨幅大于5%且成交量大于1000万手
```

### 技术指标规则
```
股价站上5日均线
股价突破20日均线
RSI大于50
MACD金叉
```

## 🔧 系统架构

```
智能股票分析系统/
├── main.py              # 主启动脚本
├── stock_analyzer.py    # 核心分析引擎
├── stock_gui.py         # 图形用户界面
├── requirements.txt     # 依赖包列表
└── README.md           # 项目文档
```

### 核心模块

- **DataProvider**: 数据提供者抽象基类
  - `AKShareProvider`: AKShare数据接口
  - `BaoStockProvider`: BaoStock数据接口

- **TechnicalAnalyzer**: 技术分析器
  - 各种技术指标计算
  - 趋势分析和信号识别

- **AIRuleParser**: AI规则解析器
  - 自然语言规则解析
  - 条件转换和验证

- **StockScreener**: 股票筛选器
  - 规则执行引擎
  - 批量股票筛选

- **StockAnalyzer**: 主分析器
  - 统一接口封装
  - 分析报告生成

## 📊 支持的数据字段

### 基本信息
- 股票代码、名称
- 当前价格、涨跌幅
- 成交量、市值
- PE、PB等估值指标

### 技术指标
- 移动平均线（MA5/10/20）
- RSI相对强弱指数
- MACD指标
- 布林带
- KDJ指标

### 历史数据
- 开盘价、最高价、最低价、收盘价
- 成交量、成交额
- 复权价格数据

## 🛠️ 自定义扩展

### 添加新的技术指标

在`TechnicalAnalyzer`类中添加新方法：

```python
@staticmethod
def calculate_custom_indicator(data: pd.Series, **kwargs) -> pd.Series:
    """自定义技术指标计算"""
    # 实现指标计算逻辑
    return result
```

### 扩展选股规则

在`AIRuleParser`类的`rule_patterns`中添加新规则：

```python
self.rule_patterns.update({
    'custom_rule': r'自定义规则正则表达式',
})
```

### 添加新数据源

继承`DataProvider`基类：

```python
class CustomDataProvider(DataProvider):
    def get_stock_list(self) -> pd.DataFrame:
        # 实现获取股票列表
        pass
    
    def get_realtime_data(self, symbols: List[str]) -> pd.DataFrame:
        # 实现获取实时数据
        pass
    
    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        # 实现获取历史数据
        pass
```

## 🐛 常见问题

### Q: 系统启动失败
A: 请检查：
1. Python版本是否 >= 3.7
2. 依赖包是否完整安装：`pip install -r requirements.txt`
3. 网络连接是否正常

### Q: 无法获取股票数据
A: 可能原因：
1. 网络连接问题
2. 数据源服务器维护
3. 请求频率过高被限制

### Q: 选股规则无法识别
A: 请确保：
1. 使用中文描述
2. 包含支持的关键词（股价、涨幅、市值等）
3. 数值格式正确

### Q: 图表显示异常
A: 请检查：
1. matplotlib是否正确安装
2. 系统是否支持GUI显示
3. 数据是否完整

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- ✅ 初始版本发布
- ✅ 支持AKShare和BaoStock数据源
- ✅ AI自然语言选股功能
- ✅ 基础技术指标分析
- ✅ GUI和CLI界面
- ✅ 数据导出功能

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## ⚠️ 免责声明

本系统仅供学习和研究使用，不构成投资建议。股市有风险，投资需谨慎。使用本系统进行投资决策的风险由用户自行承担。

## 📞 技术支持

如有问题或建议，请通过以下方式联系：

- 提交Issue
- 发送邮件
- 技术交流群

---

**🎉 感谢使用智能股票分析系统！**