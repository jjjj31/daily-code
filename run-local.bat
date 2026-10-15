@echo off
rem 手动跑一次（生成 + 提交 + 推送）
cd /d "%~dp0"
python scripts\daily_commit.py --push %*
pause
