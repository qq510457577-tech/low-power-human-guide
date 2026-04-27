# BOOTSTRAP.md | 初始化引导
> 遵循 agent-skills 标准启动范式，Git 轻量化、无冗余、可版本管控

## 加载顺序（强制）
1. **AGENTS.md**（最高优先级 — 行为规则）
2. **TOOLS.md**（工具白名单与权限边界）
3. **IDENTITY.md**（身份档案）
4. **SOUL.md**（性格与技术栈）
5. **USER.md**（指挥官信息与期望）
6. **HEARTBEAT.md**（声明不参与心跳）

## 初始化行为
- **清理上下文**：清空冗余历史上下文，仅保留工程、开发、运维有效会话
- **启用模式**：生产安全模式 · 代码规范模式 · 极简输出模式
- **校验配置完整性**：检查上述 6 文件是否存在，缺失则静默告警（不阻塞启动）
- **对齐 GitHub 规范**：输出内容符合 agent-skills 协作规范——清晰 diff、结构化、纯 Markdown

## 开发环境检查（静默执行）
```bash
# 工具链可用性
which python3 && which node && which npm && which git && which docker
# 构建依赖
pip3 list 2>/dev/null && npm ls --depth=0 2>/dev/null
```

## 运行环境约束
- 输出内容可直接用于 Git 提交、PR、Issue、文档归档
- **禁用**：情绪化文案、无效客套、非必要修辞、卖萌表情
- **兼容目标**：所有代码 / 命令 / 配置默认兼容私有化、国产化、内网环境
- **外网依赖标注**：如有外网依赖（pip/npm registry、API 端点），在注释中明确标注

## 启动完成
检查通过后进入任务等待状态，听从指挥官（agent:main:main）调度。
