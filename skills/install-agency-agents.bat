@echo off
chcp 65001 >nul
echo ==========================================
echo  Agency Agents for OpenClaw - 安装脚本
echo ==========================================
echo.

set SKILLS_DIR=%USERPROFILE%\.agents\skills
set WORKSPACE_SKILLS=%USERPROFILE%\.openclaw-autoclaw\workspace\skills

if not exist "%SKILLS_DIR%" (
    echo 创建 skills 目录...
    mkdir "%SKILLS_DIR%"
)

echo.
echo 安装 Agency Agents skills...
echo.

:: 复制前端开发技能
if exist "%WORKSPACE_SKILLS%\agency-frontend-dev" (
    xcopy /E /I /Y "%WORKSPACE_SKILLS%\agency-frontend-dev" "%SKILLS_DIR%\agency-frontend-dev" >nul
    echo ✓ 已安装: agency-frontend-dev (前端开发专家)
)

:: 复制内容创作技能
if exist "%WORKSPACE_SKILLS%\agency-content-creator" (
    xcopy /E /I /Y "%WORKSPACE_SKILLS%\agency-content-creator" "%SKILLS_DIR%\agency-content-creator" >nul
    echo ✓ 已安装: agency-content-creator (内容创作专家)
)

:: 复制冲刺规划技能
if exist "%WORKSPACE_SKILLS%\agency-sprint-prioritizer" (
    xcopy /E /I /Y "%WORKSPACE_SKILLS%\agency-sprint-prioritizer" "%SKILLS_DIR%\agency-sprint-prioritizer" >nul
    echo ✓ 已安装: agency-sprint-prioritizer (冲刺规划专家)
)

echo.
echo ==========================================
echo  安装完成！
echo ==========================================
echo.
echo 使用方法:
echo   1. 重启 OpenClaw 或刷新技能列表
echo   2. 在对话中使用:
echo      - "激活前端开发专家"
echo      - "激活内容创作专家"  
echo      - "激活冲刺规划专家"
echo.
echo 来源: https://github.com/msitarzewski/agency-agents
echo.
pause
