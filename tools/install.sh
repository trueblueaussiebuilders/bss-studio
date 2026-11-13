#!/usr/bin/env bash
# Install render dependencies (GitHub Actions runner or any Ubuntu box).
set -euo pipefail
sudo apt-get update -qq
sudo apt-get install -y -qq ffmpeg libcairo2-dev pkg-config fontconfig
mkdir -p ~/.fonts && cp assets/fonts/*.ttf ~/.fonts/ && fc-cache -f >/dev/null
pip install -q -r requirements.txt
ENGINE=${VOICE_ENGINE:-$(python3 -c "import json; print(json.load(open('voice.json')).get('engine', 'kokoro'))")}
echo "voice engine: $ENGINE"
[ "$ENGINE" = "kokoro" ] && pip install -q "kokoro-onnx>=0.4" || true
