# TOOLS.md | 工具白名单 & 权限分级
> 能力管控，最小权限原则，安全可控

## ✅ 一级开放（随时可用）
- Linux 日常排查、监控、日志分析命令
- Shell / Python / Node 常规自动化脚本
- 前后端业务代码、接口、页面开发
- 普通查询 SQL、建表、索引优化语句
- Nginx、Docker、基础服务配置
- 文档编写、架构梳理、部署方案

## ⚠️ 二级受控（需风险提示）
- 批量更新/删除数据 SQL
- 服务重启、扩容、缩容、批量容器操作
- 防火墙、权限、账号策略修改
- 线上配置热更新、流量调整

## ❌ 三级禁止（永久禁用）
- 全盘格式化、强制销毁系统指令
- 无备份删库、批量销毁数据
- 端口扫描、暴力破解、内网探测
- 后门、注入、绕过鉴权类恶意代码
- 任何违反网络安全法规的工具与脚本

## 开发环境
- **工作目录**: `/root/.openclaw/workspace-legion/dev/`
- **Server 目录**: `/root/.openclaw/workspace-legion/dev/server/`
- **前端构建输出**: `/root/.openclaw/workspace-legion/dev/dist/`

## A2A 通信
- **指挥官**: `agent:main:main`（通过 sessions_send）
- **测试工程师**: `agent:legion-test`（禁止直接通信，需指挥官协调）
- **需求分析**: `agent:legion-req`（禁止直接通信，需指挥官协调）

## 文件操作约束
- 读文件 → `read` 工具
- 写/编辑 → `write` / `edit` 工具（禁止手动 vi/nano）
- 删除 → 使用 `trash` 而非 `rm -rf`
