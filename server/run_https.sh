#!/bin/bash
# HTTPS 部署：人类低功耗生存指南 + WireGuard 页面
# 端口 8080，使用自签名证书

CERT="/etc/ssl/novnc/novnc.crt"
KEY="/etc/ssl/novnc/novnc.key"
PORT="8080"
DEEPSEEK_API_KEY="sk-fd59ba4f53954134ac48b08187b789b7"

cd "$(dirname "$0")"

# Kill ALL existing processes using the port
lsof -ti:$PORT | xargs kill -9 2>/dev/null
sleep 2

# Start with HTTPS
DEEPSEEK_API_KEY="$DEEPSEEK_API_KEY" WG_PASSWORD="openclaw@9527" nohup python3 -c "
import uvicorn
from main import app
uvicorn.run(app, host='0.0.0.0', port=$PORT, ssl_certfile='$CERT', ssl_keyfile='$KEY')
" > /tmp/lowpower-https.log 2>&1 &

echo "✅ HTTPS server starting on https://43.133.192.17:$PORT"
echo "📋 Log: /tmp/lowpower-https.log"
echo "PID: $!"
