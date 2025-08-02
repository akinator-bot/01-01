# 📱 Android APK 自动构建部署指南

本指南将帮助您将Python股票分析项目自动构建为Android APK文件。

## 🚀 快速开始

### 1. 准备GitHub仓库

1. **创建GitHub仓库**
   - 访问 [GitHub](https://github.com) 并登录
   - 创建新仓库：`https://github.com/akinator-bot/02.git`
   - 设置为公开仓库（Private仓库需要付费的GitHub Actions分钟数）

2. **上传项目文件**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Stock Analysis Android App"
   git branch -M main
   git remote add origin https://github.com/akinator-bot/02.git
   git push -u origin main
   ```

### 2. 自动构建触发

一旦代码推送到GitHub，GitHub Actions将自动开始构建APK：

- **自动触发条件**：
  - 推送到 `main` 或 `master` 分支
  - 创建版本标签（如 `v1.0.0`）
  - 手动触发（在Actions页面）

- **构建时间**：通常需要15-30分钟

### 3. 下载APK文件

#### 方式一：从Actions Artifacts下载
1. 访问仓库的 **Actions** 标签页
2. 点击最新的构建任务
3. 在 **Artifacts** 部分下载 `android-apk`

#### 方式二：从Releases下载（推荐）
1. 创建版本标签：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
2. 访问仓库的 **Releases** 页面
3. 下载最新版本的APK文件

## 📋 项目结构说明

```
股票数据安卓02/
├── main_mobile.py              # Kivy移动端主程序
├── mobile_stock_analyzer.py    # 移动端优化的分析器
├── buildozer.spec             # Android构建配置
├── requirements_mobile.txt    # 移动端依赖
├── .github/workflows/         # GitHub Actions配置
│   └── build-apk.yml         # APK构建流程
└── 原有桌面端文件...
```

## ⚙️ 构建配置详解

### buildozer.spec 关键配置

```ini
[app]
title = 智能股票分析
package.name = stockanalysis
package.domain = com.stockanalysis.app

# 应用权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 支持的架构
android.archs = arm64-v8a, armeabi-v7a

# Android版本要求
android.api = 30
android.minapi = 21
```

### GitHub Actions 工作流

构建流程包括：
1. 设置Python和Java环境
2. 安装Android SDK
3. 安装Buildozer和依赖
4. 构建APK
5. 上传到Artifacts和Releases

## 📱 APK安装说明

### 系统要求
- Android 5.0 (API 21) 或更高版本
- 至少100MB可用存储空间
- 网络连接（获取股票数据）

### 安装步骤
1. **下载APK文件**到Android设备
2. **启用未知来源安装**：
   - 设置 → 安全 → 未知来源 → 允许
   - 或者在安装时选择"仍要安装"
3. **点击APK文件**进行安装
4. **授予必要权限**（网络访问等）

## 🔧 自定义配置

### 修改应用信息

编辑 `buildozer.spec` 文件：

```ini
# 修改应用名称
title = 您的应用名称

# 修改包名
package.name = yourappname
package.domain = com.yourcompany.yourapp

# 修改版本
version = 1.0
```

### 添加应用图标

1. 准备512x512像素的PNG图标文件
2. 保存为 `icon.png`
3. 在 `buildozer.spec` 中取消注释：
   ```ini
   icon.filename = %(source.dir)s/icon.png
   ```

### 添加启动画面

1. 准备启动画面图片
2. 保存为 `presplash.png`
3. 在 `buildozer.spec` 中配置：
   ```ini
   presplash.filename = %(source.dir)s/presplash.png
   ```

## 🐛 常见问题解决

### 构建失败

1. **检查依赖库**：确保所有依赖都兼容Android
2. **查看构建日志**：在Actions页面查看详细错误信息
3. **内存不足**：可能需要减少依赖或优化代码

### APK无法安装

1. **检查Android版本**：确保设备支持API 21+
2. **存储空间**：确保有足够的安装空间
3. **权限问题**：允许安装未知来源应用

### 应用崩溃

1. **网络权限**：确保应用有网络访问权限
2. **依赖缺失**：某些Python库可能在Android上不可用
3. **内存限制**：移动设备内存有限，避免大量数据处理

## 🔄 版本发布流程

### 发布新版本

1. **更新版本号**：
   ```bash
   # 编辑 buildozer.spec
   version = 1.1
   ```

2. **提交更改**：
   ```bash
   git add .
   git commit -m "Version 1.1: 新功能描述"
   git push origin main
   ```

3. **创建版本标签**：
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

4. **自动构建**：GitHub Actions将自动构建并发布新版本

## 📊 性能优化建议

### 减小APK体积
1. 移除不必要的依赖库
2. 使用轻量级替代方案
3. 压缩资源文件

### 提升运行性能
1. 异步处理网络请求
2. 缓存常用数据
3. 优化UI响应速度

### 电池优化
1. 减少后台活动
2. 优化网络请求频率
3. 使用高效的数据结构

## 📞 技术支持

如果遇到问题，可以：

1. **查看构建日志**：GitHub Actions页面的详细日志
2. **检查Issues**：项目的GitHub Issues页面
3. **参考文档**：
   - [Buildozer文档](https://buildozer.readthedocs.io/)
   - [Kivy文档](https://kivy.org/doc/stable/)
   - [GitHub Actions文档](https://docs.github.com/en/actions)

## 🎉 完成！

现在您已经成功设置了自动化的Android APK构建流程！每次推送代码到GitHub，都会自动构建最新的APK文件。

---

**注意**：首次构建可能需要较长时间，后续构建会因为缓存而加快速度。