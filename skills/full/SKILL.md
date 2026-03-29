---
description: 完整检查 C/C++ 代码(启用所有检查项)
disable-model-invocation: false
---

执行完整代码检查:

1. 识别检查目标:
   - 如果用户提到了具体文件路径,使用该路径
   - 如果当前有打开的 C/C++ 文件,检查该文件
   - 否则检查当前工作目录

2. 调用 check_code 工具:
   - target_path: 使用识别的目标路径(必须是绝对路径)
   - mode: "full"

3. 分析检查结果:
   - 按严重程度分类问题(error, warning, style, performance, portability，information)
   - 统计各类问题数量
   - 列出所有重要问题

4. 提供详细建议:
   - 优先级排序(先修复 error,再处理 warning)
   - 对于 style 和 performance 问题,说明影响
   - 如果问题过多,建议分批处理
