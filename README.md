# MCP Cppcheck Plugin

这是一个基于 MCP (Model Context Protocol) 的 cppcheck 静态代码检查插件,为 Claude Code 提供智能化的 C/C++ 代码分析能力。

## 项目概述

**目标**: 将 cppcheck 工具封装为 MCP 服务,提供项目感知、输出优化和智能化检查能力,使其更适合 LLM 使用。

**核心特性**:
- 自动检测项目配置(compile_commands.json、.cppcheck)
- 智能识别项目根目录和项目类型
- XML 输出清洗(移除冗余信息)
- 路径规范化(支持相对路径自动转换)
- 跨平台支持(Windows/Linux/macOS)

## 项目结构

```
cpp-checker/
├── mcp_cppcheck/              # MCP 服务器核心
│   ├── src/mcp_cppcheck/
│   │   ├── server.py          # FastMCP 服务器定义
│   │   ├── cppcheck_runner.py # cppcheck 执行和输出清洗
│   │   ├── project_detector.py # 项目配置检测
│   │   └── __main__.py        # 入口点
│   ├── README.md              # 安装和配置说明
│   └── REQUIREMENTS.md        # 详细需求文档(中文)
├── hooks/                     # Claude Code hooks
│   ├── cppcheck-path-resolver-debug.py  # PreToolUse hook: 路径规范化
│   └── hooks.json             # Hook 配置(默认关闭)
├── skills/                    # Claude Code skills
│   ├── hello/                 # 示例 skill
│   ├── help/                  # 帮助 skill
│   ├── quick/                 # 快速检查 skill
│   └── full/                  # 完整检查 skill
├── agents/                    # Claude Code subagents
│   └── cppcheck-assistant.md  # 代码检查和修复助手
├── .claude-plugin/            # Claude 插件元数据
│   └── plugin.json
└── .mcp.json                  # MCP 服务器配置
```

## MCP 工具接口

### 1. check_code
检查 C/C++ 代码文件或目录

**参数**:
- `target_path` (string, 必需): 文件/目录的**绝对路径**,或项目文件路径(compile_commands.json/.cppcheck/.sln等)
- `mode` (string, 可选): 检查模式
  - `"quick"` (默认): 快速检查,只启用 warning 级别
  - `"full"`: 完整检查,启用所有检查项(--enable=all)

**行为**:
- 自动检测是否为项目文件(compile_commands.json/.cppcheck/.sln/.vcxproj等)
- 如果是项目文件,使用 `--project` 参数
- 否则自动搜索 compile_commands.json 并应用
- 自动添加项目根目录为 include 路径(-I)
- 返回清洗后的 XML 格式结果(移除 verbose 和 column 属性)

**重要**: target_path 必须是绝对路径。相对路径会被 PreToolUse hook 自动转换。

### 2. get_project_context
获取项目配置信息(调试用)

**参数**:
- `target_path` (string, 必需): 文件或目录路径

**返回**: JSON 格式的项目信息
- `is_project_file`: 是否为项目文件
- `project_root`: 检测到的项目根目录
- `compile_commands`: compile_commands.json 路径(如果找到)
- `cppcheck_config`: .cppcheck 配置文件路径(如果找到)

## 核心模块说明

### ProjectContext (project_detector.py)
**职责**: 项目配置检测和上下文信息收集

**关键逻辑**:
1. **路径规范化**: 处理 Git Bash 风格路径(/d/path -> D:/path)
2. **项目文件识别**: 检测 .sln/.vcxproj/compile_commands.json/.cppcheck 等
3. **项目根目录查找**:
   - 优先级标记: .git, Makefile, .cppcheck, meson.build, configure.ac, *.sln
   - 次优先: 最顶层的 CMakeLists.txt
   - 兜底: 目标文件所在目录
4. **配置文件搜索**: 在项目根目录和 build*/cmake-build*/out* 目录中查找

### CppcheckRunner (cppcheck_runner.py)
**职责**: 构建 cppcheck 命令并清洗输出

**命令构建逻辑**:
```python
# 基础命令
cppcheck --xml --xml-version=2

# 模式选择
--enable=warning  # quick 模式
--enable=all      # full 模式

# 项目文件优先
--project=<project_file>  # 如果是项目文件

# 否则使用 compile_commands.json
--project=<compile_commands.json>

# 兜底: 添加项目根目录为 include 路径
-I<project_root> <target_path>
```

**XML 清洗**:
- 移除 `<error>` 的 `verbose` 属性(冗余的详细说明)
- 移除 `<location>` 的 `column` 属性(列号信息)
- 保留: id, severity, msg, file, line

## Hooks

### cppcheck-path-resolver-debug.py
**触发时机**: PreToolUse (在 MCP 工具调用前)

**状态**: 默认关闭 (`disabled: true`，由于PreToolUse串联调用存在的覆盖问题)

**功能**:
- 检测 cppcheck 工具调用
- 将相对路径的 `target_path` 转换为绝对路径
- 使用当前工作目录(cwd)进行路径解析
- 记录日志到 `hooks/hook.log`

**为什么需要**: MCP 工具要求绝对路径,但用户可能提供相对路径。Hook 自动规范化路径,提升用户体验。

## 技术栈

- **Python**: >= 3.10
- **MCP SDK**: FastMCP (简化的 MCP 服务器开发方式)
- **包管理**: uv
- **外部依赖**: cppcheck (需单独安装)
- **平台**: Windows/Linux/macOS

## 使用场景

1. **LLM 辅助代码审查**: Claude 调用 check_code 分析代码,提供修复建议
2. **项目级静态分析**: 自动检测项目配置,应用正确的检查策略
3. **CI/CD 集成**: 通过 MCP 协议提供统一接口
4. **IDE 集成**: 实时代码检查和智能提示

## Skills

插件提供以下 skills 简化使用:

### 已实现的 Skills

**help** (`/cpp-checker:help`):
- 显示插件使用指南和功能特性
- `disable-model-invocation: false` - 允许 LLM 交互式回答问题

**quick** (`/cpp-checker:quick`):
- 快速检查当前文件或项目(warning 级别)
- 自动识别检查目标(当前文件/工作目录)
- 调用 `check_code` 工具,mode="quick"
- 分析结果并提供简要总结

**full** (`/cpp-checker:full`):
- 完整检查当前文件或项目(所有检查项)
- 检测 error、warning、style、performance、portability、information
- 按严重程度分类问题并提供详细建议

### 未来 Skills 计划

- `cppcheck-fix`: 检查并提供修复建议
- `cppcheck-config`: 配置 cppcheck 规则

## Subagents

插件提供以下 subagent 用于独立上下文中的复杂任务:

### cppcheck-assistant

**位置**: `agents/cppcheck-assistant.md`

**配置**:
- 模型: `sonnet` (平衡性能和成本)
- 可用工具: check_code, get_project_context, Read, Grep, Glob, Edit, Write

**功能**:
- 代码检查: 调用 check_code 工具分析 C/C++ 代码
- 问题修复: 识别问题并提供具体修复方案
- 报告生成: 生成结构化的 Markdown 检查报告

**使用场景**:
- 需要深度分析大型项目
- 批量处理多个文件的检查结果
- 生成详细的代码质量报告

**工作模式**:
1. 检查模式 - 执行代码检查并分类问题
2. 修复模式 - 提供针对性的修复建议
3. 报告模式 - 生成完整的检查报告

## 开发指南

### 安装开发环境
```bash
cd mcp_cppcheck
uv pip install -e .
```

### 本地测试
```bash
# 测试 MCP 工具
python test_local.py

# 查看项目上下文
python -m mcp_cppcheck
```

### 添加新 Skill
1. 在 `skills/` 目录创建新文件夹
2. 添加 `SKILL.md` 定义 skill 行为
3. 在 SKILL.md 中引用 MCP 工具

### 添加新 Hook
1. 在 `hooks/` 目录创建 Python 脚本
2. 在 `hooks/hooks.json` 中注册
3. 遵循 Claude Code hook 协议


## 相关文档

- `mcp_cppcheck/README.md`: 安装和配置说明
- `mcp_cppcheck/REQUIREMENTS.md`: 详细需求文档(中文)
- [Cppcheck 官方文档](http://cppcheck.net/)
- [MCP 协议规范](https://modelcontextprotocol.io/)
