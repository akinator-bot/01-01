# 📱 智能股票分析 - Android版

基于AI的智能股票分析系统，现已支持Android平台！通过自然语言描述选股规则，轻松进行股票筛选和分析。

## ✨ 主要特性

- 🤖 **AI驱动选股**：用自然语言描述选股条件
- 📊 **实时数据**：集成BaoStock数据源
- 📱 **移动优化**：专为Android设备优化的界面
- 🔄 **自动构建**：GitHub Actions自动生成APK
- 🎯 **轻量级**：针对移动设备性能优化

## 🚀 快速体验

### 下载APK

1. 访问 [Releases页面](https://github.com/akinator-bot/02/releases)
2. 下载最新版本的APK文件
3. 在Android设备上安装

### 系统要求

- Android 5.0 (API 21) 或更高版本
- 网络连接
- 至少100MB可用存储空间

## 📖 使用指南

### 智能选股

使用自然语言描述选股条件，例如：

- "市盈率小于20且成交量大于平均值"
- "股价在20日均线之上的科技股"
- "近期涨幅超过5%的小盘股"

### 个股分析

输入股票代码（如：000001）获取详细分析：

- 基本面信息
- 技术指标
- 价格趋势
- 成交量分析

## 🛠️ 开发者指南

### 项目结构

```
├── main_mobile.py              # Kivy移动端主程序
├── mobile_stock_analyzer.py    # 移动端分析器
├── buildozer.spec             # Android构建配置
├── requirements_mobile.txt    # 移动端依赖
└── .github/workflows/         # 自动构建配置
    └── build-apk.yml
```

### 本地开发

1. **安装依赖**：
   ```bash
   pip install -r requirements_mobile.txt
   ```

2. **运行应用**：
   ```bash
   python main_mobile.py
   ```

### 构建APK

详细构建说明请参考 [ANDROID_DEPLOYMENT.md](ANDROID_DEPLOYMENT.md)

## 🔧 技术栈

- **UI框架**：Kivy (跨平台)
- **数据源**：BaoStock API
- **数据处理**：Pandas, NumPy
- **构建工具**：Buildozer
- **CI/CD**：GitHub Actions

## 📊 功能对比

| 功能 | 桌面版 | Android版 |
|------|--------|----------|
| 自然语言选股 | ✅ | ✅ |
| 个股分析 | ✅ | ✅ |
| 数据可视化 | 复杂图表 | 简化图表 |
| 数据导出 | 多格式 | 基础格式 |
| 界面 | tkinter | Kivy |
| 性能 | 高 | 优化 |

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [BaoStock](http://baostock.com/) - 提供股票数据API
- [Kivy](https://kivy.org/) - 跨平台UI框架
- [Buildozer](https://github.com/kivy/buildozer) - Android打包工具

---

**注意**：本应用仅供学习和研究使用，不构成投资建议。投资有风险，入市需谨慎。