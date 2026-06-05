@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "SKILLS_DIR=%SCRIPT_DIR%skills"

if "%~1"=="" goto usage
if /i "%~1"=="help" goto usage
if "%~1"=="/?" goto usage

set "TARGET=%~1"
set "SKILL_FILTER=%~2"

if /i "%TARGET%"=="codex"  goto do_codex
if /i "%TARGET%"=="claude" goto do_claude
if /i "%TARGET%"=="all"    goto do_all
goto usage

:: ── helpers ──────────────────────────────────────────────────────────────────

:install_all_to
:: %1 = target base dir,  %2 = skill filter (may be empty)
set "BASE=%~1"
for /d %%S in ("%SKILLS_DIR%\*") do (
  set "SKILL_NAME=%%~nxS"
  if not exist "%%S\SKILL.md" (
    echo   [skip] !SKILL_NAME!: SKILL.md not found
  ) else (
    if "%~2"=="" (
      call :install_one "%BASE%" "!SKILL_NAME!"
    ) else (
      if /i "!SKILL_NAME!"=="%~2" call :install_one "%BASE%" "!SKILL_NAME!"
    )
  )
)
goto :eof

:install_one
:: %1 = target base dir,  %2 = skill name
set "DEST=%~1\%~2"
if not exist "%DEST%" mkdir "%DEST%"
copy /y "%SKILLS_DIR%\%~2\SKILL.md" "%DEST%\SKILL.md" >nul
echo   OK  %DEST%\SKILL.md
goto :eof

:: ── targets ──────────────────────────────────────────────────────────────────

:do_codex
echo =^>^> Codex
call :install_all_to "%USERPROFILE%\.agents\skills" "%SKILL_FILTER%"
call :install_all_to "%USERPROFILE%\.codex\skills"  "%SKILL_FILTER%"
goto done

:do_claude
echo =^>^> Claude Code
call :install_all_to "%USERPROFILE%\.claude\skills" "%SKILL_FILTER%"
goto done

:do_all
echo =^>^> Codex
call :install_all_to "%USERPROFILE%\.agents\skills" "%SKILL_FILTER%"
call :install_all_to "%USERPROFILE%\.codex\skills"  "%SKILL_FILTER%"
echo =^>^> Claude Code
call :install_all_to "%USERPROFILE%\.claude\skills" "%SKILL_FILTER%"
goto done

:done
echo.
echo Done.
goto :eof

:: ── usage ─────────────────────────────────────────────────────────────────────

:usage
echo Usage: install.bat [codex^|claude^|all] [^<skill-name^>]
echo.
echo   codex   Install for Codex      (%%USERPROFILE%%\.agents\skills\, %%USERPROFILE%%\.codex\skills\)
echo   claude  Install for Claude Code (%%USERPROFILE%%\.claude\skills\)
echo   all     Install for all supported tools
echo.
echo   Optional second argument: install only the named skill
echo.
echo Available skills:
for /d %%S in ("%SKILLS_DIR%\*") do (
  if exist "%%S\SKILL.md" echo   - %%~nxS
)
exit /b 1
