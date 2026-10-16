#!/usr/bin/env bash
# 删除超过指定天数的日志文件
set -euo pipefail

LOG_DIR="${1:-/var/log/app}"
KEEP_DAYS="14"

find "$LOG_DIR" -type f -name "*.log" -mtime "+$KEEP_DAYS" -print -delete
echo "cleaned logs older than $KEEP_DAYS days in $LOG_DIR"
