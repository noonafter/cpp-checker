---
description: 快速检查 C/C++ 代码(warning 级别)
disable-model-invocation: false
---

执行快速代码检查:

1. 识别检查目标:
   - 如果用户提到了具体文件路径,使用该路径
   - 如果当前有打开的 C/C++ 文件,检查该文件
   - 否则检查当前工作目录

2. 调用 check_code 工具:
   - target_path: 使用识别的目标路径(必须是绝对路径)
   - mode: "quick"

3. 分析检查结果:
   - 总结发现的问题数量和类型
   - 列出关键问题(severity 为 error 或 warning)
   - 如果没有问题,告知用户代码检查通过

4. 提供建议:
   - 如果有严重问题,建议优先修复
   - 如果需要更详细检查,建议使用 /cpp-checker:full
