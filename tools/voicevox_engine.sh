#!/usr/bin/env bash
# VOICEVOX公式エンジン(Docker Hub: voicevox/voicevox_engine, CPU版)を
# このマシン内だけ(127.0.0.1:50021)で起動する。未取得なら公式イメージから取り出す。
# 使い方: bash tools/voicevox_engine.sh   （すでに起動済みなら何もしない）
set -euo pipefail

PORT=50021
CACHE="${VOICEVOX_CACHE:-/tmp/voicevox_engine}"
ENGINE_DIR="$CACHE/root/opt/voicevox_engine"
REPO="voicevox/voicevox_engine"
TAG="cpu-latest"

if curl -s --noproxy 127.0.0.1 "http://127.0.0.1:$PORT/version" >/dev/null 2>&1; then
  echo "VOICEVOX engine already running: $(curl -s --noproxy 127.0.0.1 http://127.0.0.1:$PORT/version)"
  exit 0
fi

# 以前このセッションで展開した場所があれば再利用
if [ ! -x "$ENGINE_DIR/run" ] && [ -x /tmp/claude-0/vv/root/opt/voicevox_engine/run ]; then
  ENGINE_DIR=/tmp/claude-0/vv/root/opt/voicevox_engine
fi

if [ ! -x "$ENGINE_DIR/run" ]; then
  echo "Fetching official image $REPO:$TAG from Docker Hub ..."
  mkdir -p "$CACHE/root"
  TOKEN=$(curl -sS "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$REPO:pull" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
  AUTH="Authorization: Bearer $TOKEN"
  REG="https://registry-1.docker.io/v2/$REPO"
  DIGEST=$(curl -sS -H "$AUTH" \
    -H "Accept: application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json" \
    "$REG/manifests/$TAG" | python3 -c "
import json,sys
for m in json.load(sys.stdin)['manifests']:
    if m['platform']['architecture']=='amd64': print(m['digest'])")
  # 全レイヤーを順に展開（エンジン本体は最大のレイヤーに入っている）
  curl -sS -H "$AUTH" -H "Accept: application/vnd.oci.image.manifest.v1+json" "$REG/manifests/$DIGEST" \
    | python3 -c "import json,sys;[print(l['digest']) for l in json.load(sys.stdin)['layers']]" \
    | while read -r layer; do
        curl -sSL -H "$AUTH" "$REG/blobs/$layer" | tar -xz -C "$CACHE/root" 2>/dev/null || true
      done
fi

cd "$ENGINE_DIR"
nohup ./run --host 127.0.0.1 --port "$PORT" > "$CACHE.log" 2>&1 &
for _ in $(seq 1 90); do
  if curl -s --noproxy 127.0.0.1 "http://127.0.0.1:$PORT/version" >/dev/null 2>&1; then
    echo "VOICEVOX engine started: $(curl -s --noproxy 127.0.0.1 http://127.0.0.1:$PORT/version)"
    exit 0
  fi
  sleep 2
done
echo "VOICEVOX engine failed to start; see $CACHE.log" >&2
exit 1
