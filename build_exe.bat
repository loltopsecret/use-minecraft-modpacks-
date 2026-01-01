@echo off
chcp 65001 >nul
cls

:action_selection
echo ========================================
echo    What are we doing today?
echo ========================================
echo.
echo 1. Installing
echo 2. Deleting (build files only)
echo 3. Full cleanup (including Python libraries)
echo.
set /p action_choice="Select action (1/2/3): "

if "%action_choice%"=="1" goto language_selection
if "%action_choice%"=="2" goto delete_files
if "%action_choice%"=="3" goto full_cleanup

echo Invalid choice
timeout /t 2 >nul
goto action_selection

:delete_files
echo.
echo Deleting build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist  
if exist *.spec del /q *.spec
if exist config.json del /q config.json
echo.
echo ========================================
echo    Build files deleted successfully!
echo ========================================
echo.
pause
exit

:full_cleanup
echo.
echo ========================================
echo    WARNING: This will uninstall Python libraries!
echo ========================================
echo.
echo This will remove:
echo - pyinstaller
echo - pillow
echo - All build files
echo.
set /p confirm="Are you sure? (y/n): "

if /i "%confirm%" NEQ "y" (
    echo Cancelled.
    timeout /t 2 >nul
    exit
)

echo.
echo Uninstalling Python libraries...
pip uninstall -y pyinstaller
pip uninstall -y pillow

echo.
echo Deleting all files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
if exist config.json del /q config.json

echo.
echo ========================================
echo    Full cleanup completed!
echo ========================================
echo.
pause
exit

:language_selection
echo ========================================
echo    Language Selection / Выбор языка
echo ========================================
echo.
echo 1. English
echo 2. Русский
echo.
set /p lang_choice="Select language / Выберите язык (1/2): "

if "%lang_choice%"=="1" goto build_en
if "%lang_choice%"=="2" goto build_ru

echo Invalid choice / Неверный выбор
timeout /t 2 >nul
goto language_selection

:build_en
cls
echo ========================================
echo    Building EXE for Minecraft Modpack Archiver
echo ========================================
echo.

if exist "dist\minecraft_modpack_archiver DEBUG.py" (
    echo Found: dist\minecraft_modpack_archiver DEBUG.py
    set PYFILE=dist\minecraft_modpack_archiver DEBUG.py
) else if exist "dist\minecraft_modpack_archiver.py" (
    echo Found: dist\minecraft_modpack_archiver.py
    set PYFILE=dist\minecraft_modpack_archiver.py
) else if exist minecraft_modpack_archiver.py (
    echo Found: minecraft_modpack_archiver.py
    set PYFILE=minecraft_modpack_archiver.py
) else (
    echo ERROR: Python file not found!
    pause
    exit
)

echo Checking installations...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

pip show pillow >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Pillow...
    pip install pillow
)

echo.
echo Building EXE...
pyinstaller --onefile --windowed --name=MinecraftModpackArchiver_EN --distpath . "%PYFILE%"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    SUCCESS!
    echo ========================================
    echo.
    echo File: MinecraftModpackArchiver_EN.exe
    pause
    explorer .
) else (
    echo.
    echo ERROR creating EXE
    pause
)
exit

:build_ru
cls
echo ========================================
echo    Сборка EXE для Архиватора модпаков
echo ========================================
echo.

if exist "dist\minecraft_modpack_archiver DEBUG.py" (
    echo Найден: dist\minecraft_modpack_archiver DEBUG.py
    set PYFILE=dist\minecraft_modpack_archiver DEBUG.py
) else if exist "dist\minecraft_modpack_archiver.py" (
    echo Найден: dist\minecraft_modpack_archiver.py
    set PYFILE=dist\minecraft_modpack_archiver.py
) else if exist minecraft_modpack_archiver.py (
    echo Найден: minecraft_modpack_archiver.py
    set PYFILE=minecraft_modpack_archiver.py
) else (
    echo ОШИБКА: Python файл не найден!
    pause
    exit
)

echo Проверка установок...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Установка PyInstaller...
    pip install pyinstaller
)

pip show pillow >nul 2>&1
if %errorlevel% neq 0 (
    echo Установка Pillow...
    pip install pillow
)

echo.
echo Сборка EXE...
pyinstaller --onefile --windowed --name=MinecraftModpackArchiver_RU --distpath . "%PYFILE%"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    УСПЕШНО!
    echo ========================================
    echo.
    echo Файл: MinecraftModpackArchiver_RU.exe
    pause
    explorer .
) else (
    echo.
    echo ОШИБКА создания EXE
    pause
)
exit