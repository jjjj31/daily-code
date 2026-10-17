#!/usr/bin/env bash
# 批量探测端口是否可连接
set -uo pipefail

HOST="${1:-127.0.0.1}"
PORTS=(22 443 3306 9000)

for port in "${PORTS[@]}"; do
    if (echo > "/dev/tcp/$HOST/$port") >/dev/null 2>&1; then
        echo "$port open"
    else
        echo "$port closed"
    fi
done
