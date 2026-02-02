#!/bin/bash

# =================配置区域=================
APP_NAME="milvus-lite"
ENTRY_POINT="main.py"
# =========================================

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}==> 开始打包流程: ${APP_NAME}${NC}"

# 清理
rm -rf dist build *.spec __pycache__ modules/__pycache__ api/__pycache__

# 生成 Spec 文件
cat > ${APP_NAME}.spec <<EOF
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules
import sys
import os

block_cipher = None

# --- 核心配置 ---

# 1. 收集 Milvus Lite (必须)
datas_milvus, binaries_milvus, hiddenimports_milvus = collect_all('milvus_lite')

# 2. 收集 Uvicorn (必须，解决找不到 loop 等问题)
hiddenimports_uvicorn = collect_submodules('uvicorn')

# 3. 其他手动隐式导入
manual_hidden_imports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan.on',
    'jinja2',
]

# 合并配置 (已移除 api 的强制收集)
combined_hiddenimports = (
    hiddenimports_milvus +
    hiddenimports_uvicorn +
    manual_hidden_imports
)

combined_datas = datas_milvus
combined_binaries = binaries_milvus

a = Analysis(
    ['${ENTRY_POINT}'],
    pathex=[],
    binaries=combined_binaries,
    datas=combined_datas,
    hiddenimports=combined_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --- EXE 配置：排除二进制，只做引导 ---
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True, # 文件夹模式关键配置
    name='${APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# --- COLLECT 配置：生成文件夹 ---
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='${APP_NAME}', # dist 下生成的文件夹名称
)
EOF

# 执行打包
pyinstaller --clean --noconfirm --log-level=WARN ${APP_NAME}.spec

if [ $? -eq 0 ]; then
    echo -e "${GREEN}==> 打包成功!${NC}"
    echo -e "程序目录: ${GREEN}dist/${APP_NAME}/${NC}"
    echo -e "启动命令: ${GREEN}./dist/${APP_NAME}/${APP_NAME}${NC}"
else
    echo "打包失败"
    exit 1
fi