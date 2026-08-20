@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title GptNotion Local MCP 4.0

echo ========================================================================
echo GptNotion Local MCP 4.0 ^| Universal Model Gateway + SQLite + Agent Jobs
echo ========================================================================
echo.
echo [1] SQLite local DB
echo [2] MCP tools / agent jobs
echo [3] Universal Model Gateway - Chat / Responses / Completions / Ollama
echo [4] Model compatibility profile / JSON repair / adaptive tool routing
echo.

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0gptnotion_local_mcp.py"
  goto :end
)
where python >nul 2>nul
if %errorlevel%==0 (
  python "%~dp0gptnotion_local_mcp.py"
  goto :end
)

echo [오류] Python 3을 찾을 수 없습니다.
echo Python 3 설치 후 다시 실행해 주세요.
echo SQLite는 별도 설치할 필요가 없습니다. Python sqlite3를 사용합니다.
pause
:end
if not %errorlevel%==0 pause
endlocal
