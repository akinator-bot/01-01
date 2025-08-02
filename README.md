# 智能股票分析 Android 应用

## 项目概述

这是一个基于 Kivy 框架开发的 Android 股票分析应用，提供智能选股和个股分析功能。

## 🔧 问题修复记录

### 主要问题分析

原项目在 GitHub Actions 构建时频繁失败，根本原因是：

1. **架构问题**：试图将复杂的桌面数据分析系统直接移植到移动端
2. **依赖问题**：使用了 `pandas` 和 `numpy` 等需要 C 扩展编译的重型库
3. **构建配置**：GitHub Actions 工作流过于复杂，NDK/SDK 配置不当

### 解决方案

#### 1. 移除重型依赖
- ❌ 移除 `pandas`：使用 Python 标准库 `statistics` 替代
- ❌ 移除 `numpy`：使用 Python 标准库 `random` 替代
- ❌ 移除 `matplotlib`、`seaborn`：移动端不需要复杂图表
- ❌ 移除 `akshare`：依赖过多，使用简化数据源

#### 2. 简化项目架构
- ✅ 保留核心功能：智能选股、个股分析
- ✅ 使用轻量级依赖：`kivy`、`requests`、`baostock`
- ✅ 实现数据回退机制：真实数据获取失败时使用模拟数据

#### 3. 优化构建配置
- ✅ 使用官方 `ArtemSBulgakov/buildozer-action`
- ✅ 简化 GitHub Actions 工作流
- ✅ 使用稳定的 Android API 级别（21-28）
- ✅ 让 buildozer 自动处理 NDK 下载

## 📱 功能特性

- **智能选股**：支持自然语言输入选股规则
- **个股分析**：提供基本的股票信息分析
- **移动优化**：专为 Android 设备优化的界面
- **离线支持**：网络不可用时使用模拟数据

## 🛠️ 技术栈

- **框架**：Kivy 2.1+
- **网络**：requests
- **数据源**：baostock（可选）
- **语言**：Python 3.9+
- **构建工具**：buildozer

## 📦 项目结构

```
.
├── main_mobile.py          # 主应用入口
├── mobile_stock_analyzer.py # 核心分析模块
├── buildozer.spec          # 构建配置
├── requirements.txt        # 依赖列表
├── test_mobile.py          # 测试脚本
└── .github/workflows/
    └── build-apk.yml       # GitHub Actions 工作流
```

## 🚀 构建说明

### 本地构建

1. 安装 buildozer：
```bash
pip install buildozer
```

2. 构建 APK：
```bash
buildozer android debug
```

### GitHub Actions 自动构建

推送到 `main` 分支时会自动触发构建，生成的 APK 文件可在 Actions 页面下载。

## 📋 系统要求

- **Android**：5.0 (API 21) 或更高版本
- **权限**：网络访问、存储访问
- **网络**：可选（有网络时获取真实数据，无网络时使用模拟数据）

## 🔍 测试

运行测试脚本验证配置：
```bash
python test_mobile.py
```

## 📝 更新日志

### v1.0 (当前版本)
- ✅ 完全移除 pandas/numpy 依赖
- ✅ 简化 GitHub Actions 工作流
- ✅ 优化 buildozer 配置
- ✅ 实现轻量级数据处理
- ✅ 添加完整的错误处理和回退机制

## ⚠️ 注意事项

1. **首次启动**：可能需要较长时间初始化
2. **网络连接**：建议在有网络环境下使用以获取最新数据
3. **数据准确性**：模拟数据仅用于演示，实际投资请参考专业平台
4. **安装来源**：需要允许安装未知来源应用

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 📄 许可证

MIT License