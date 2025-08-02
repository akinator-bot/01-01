#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions 构建状态检查脚本
帮助监控Android APK构建进度
"""

import requests
import json
import time
from datetime import datetime

# GitHub仓库信息（需要根据实际情况修改）
REPO_OWNER = "akinator-bot"
REPO_NAME = "01-01"
WORKFLOW_NAME = "build-apk.yml"

def get_latest_workflow_run():
    """获取最新的workflow运行状态"""
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            runs = data.get('workflow_runs', [])
            
            if runs:
                latest_run = runs[0]
                return {
                    'id': latest_run['id'],
                    'status': latest_run['status'],
                    'conclusion': latest_run['conclusion'],
                    'created_at': latest_run['created_at'],
                    'updated_at': latest_run['updated_at'],
                    'html_url': latest_run['html_url'],
                    'head_commit': latest_run['head_commit']['message'][:100] if latest_run.get('head_commit') else 'N/A'
                }
        else:
            print(f"API请求失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"获取workflow状态失败: {e}")
        return None

def format_time(iso_time):
    """格式化时间显示"""
    try:
        dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return iso_time

def get_status_emoji(status, conclusion):
    """根据状态返回对应的emoji"""
    if status == 'completed':
        if conclusion == 'success':
            return '✅'
        elif conclusion == 'failure':
            return '❌'
        elif conclusion == 'cancelled':
            return '⏹️'
        else:
            return '⚠️'
    elif status == 'in_progress':
        return '🔄'
    elif status == 'queued':
        return '⏳'
    else:
        return '❓'

def main():
    """主函数"""
    print("GitHub Actions 构建状态检查器")
    print(f"仓库: {REPO_OWNER}/{REPO_NAME}")
    print("=" * 60)
    
    while True:
        run_info = get_latest_workflow_run()
        
        if run_info:
            emoji = get_status_emoji(run_info['status'], run_info['conclusion'])
            
            print(f"\n{emoji} 最新构建状态:")
            print(f"  ID: {run_info['id']}")
            print(f"  状态: {run_info['status']}")
            if run_info['conclusion']:
                print(f"  结果: {run_info['conclusion']}")
            print(f"  创建时间: {format_time(run_info['created_at'])}")
            print(f"  更新时间: {format_time(run_info['updated_at'])}")
            print(f"  提交信息: {run_info['head_commit']}")
            print(f"  查看详情: {run_info['html_url']}")
            
            if run_info['status'] == 'completed':
                if run_info['conclusion'] == 'success':
                    print("\n🎉 构建成功！APK应该已经生成。")
                    print("请到GitHub Actions页面下载APK文件。")
                elif run_info['conclusion'] == 'failure':
                    print("\n💥 构建失败，请检查日志。")
                    print("常见问题解决方案:")
                    print("1. 检查buildozer.spec配置")
                    print("2. 确认所有依赖都是纯Python包")
                    print("3. 查看GitHub Actions日志获取详细错误信息")
                break
            elif run_info['status'] == 'in_progress':
                print("\n⏳ 构建进行中，请稍候...")
            elif run_info['status'] == 'queued':
                print("\n📋 构建已排队，等待开始...")
        else:
            print("❌ 无法获取构建状态")
        
        print("\n按Ctrl+C退出，或等待30秒后自动刷新...")
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n👋 退出监控")
            break
        
        # 清屏（Windows）
        import os
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        
        print("GitHub Actions 构建状态检查器")
        print(f"仓库: {REPO_OWNER}/{REPO_NAME}")
        print("=" * 60)

if __name__ == "__main__":
    main()