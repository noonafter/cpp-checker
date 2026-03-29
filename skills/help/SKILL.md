---
description: 显示 cpp-checker 插件的帮助信息和使用指南
disable-model-invocation: false
---

# MCP Cppcheck 插件使用指南

这是一个基于 MCP 的 cppcheck 静态代码检查插件,为 C/C++ 代码提供智能化分析。

## 可用命令

- `/cpp-checker:help` - 显示此帮助信息
- `/cpp-checker:quick` - 快速检查当前文件或项目，只检测error和warning级别问题，用时较短
- `/cpp-checker:full` - 完整检查当前文件或项目，检测包括error、warning、style、performance、portability和information在内的问题，用时较长

## 使用示例

```
- 快速检查当前目录代码
- 完整检查当前目录代码
- 使用 check_code 工具检查 /path/to/file.cpp
- 显示cpp-checker插件的帮助
```

## 功能特性

- 自动检测项目配置 (compile_commands.json, .cppcheck)
- 智能识别项目根目录
- 输出优化 (移除冗余信息)
- 跨平台支持 (Windows/Linux/macOS)

需要更多帮助?请查看项目文档或访问项目地址：https://github.com/noonafter/cpp-checker
