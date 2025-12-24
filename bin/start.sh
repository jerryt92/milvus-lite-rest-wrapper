#!/bin/zsh
# 获取当前目录
dir=$(cd "$(dirname "$0")"; pwd)
# 去到上级目录
cd $dir/..
uvicorn main:app --reload