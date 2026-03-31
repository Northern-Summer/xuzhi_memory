#!/bin/bash
# Xuzhi System Repair — Shell wrapper
# 用法: bash system_repair.sh [--diagnose] [--fix] [--commit]
cd ~/.xuzhi_memory
python3 system_repair.py "$@"
