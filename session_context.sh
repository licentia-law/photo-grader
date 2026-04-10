#!/bin/bash
# Photo Color Grading Tool — 세션 시작 컨텍스트 스크립트
# 사용법: source session_context.sh (프로젝트 루트에서 실행)

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=== Photo Color Grading Tool ==="
echo "Project Root: $PROJECT_ROOT"
echo ""

# 현재 Phase 표시
echo "--- 현재 개발 Phase ---"
cat "$PROJECT_ROOT/current_phase.txt"
echo ""

# Python 환경 확인
echo "--- Python 환경 ---"
VENV_PATH="$PROJECT_ROOT/backend/.venv"
if [ -d "$VENV_PATH" ]; then
  echo "✓ .venv 존재: $VENV_PATH"
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source "$VENV_PATH/Scripts/activate"
  else
    source "$VENV_PATH/bin/activate"
  fi
  python --version
  echo "✓ .venv 활성화 완료"
else
  echo "✗ .venv 없음 — 아래 명령어로 생성:"
  echo "  cd backend && python -m venv .venv"
fi
echo ""

# Node.js 환경 확인
echo "--- Node.js 환경 ---"
export PATH="$PATH:/c/Program Files/nodejs"
if command -v node &>/dev/null; then
  echo "✓ Node.js: $(node --version)"
  echo "✓ npm: $(npm --version)"
else
  echo "✗ Node.js 미설치"
fi
echo ""

# 파일 구조 요약
echo "--- 백엔드 파일 현황 ---"
ls "$PROJECT_ROOT/backend/" 2>/dev/null | grep -v ".venv" | grep -v "__pycache__"
echo ""
echo "--- 프론트엔드 src 현황 ---"
ls "$PROJECT_ROOT/frontend/src/" 2>/dev/null
echo ""

echo "=== 준비 완료. CLAUDE.md와 current_phase.txt를 참고하세요. ==="
