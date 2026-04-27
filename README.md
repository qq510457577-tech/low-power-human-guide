# 🧘 人类低功耗生存指南

> **心外无物 · 以最少消耗活出最自在的人生**

以王阳明"心外无物"为哲学内核的健康生活方式 Web 项目。纯静态部署，零后端成本。

## 🌐 访问

- **GitHub Pages**: https://qq510457577-tech.github.io/low-power-human-guide/
- **源码**: https://github.com/qq510457577-tech/low-power-human-guide

## 📄 页面

| 页面 | 路径 | 功能 |
|------|------|------|
| 首页 | `/` | 哲学理念 + 三大支柱入口 |
| 低功耗自测 | `/self-test` | 8题5级评分自测问卷 |
| 每日微行动 | `/daily-actions` | 22个微行动 + 每日推荐 + 进度追踪 |
| 指南文章 | `/articles` | 12篇分类文章 + 搜索过滤 |
| 文章详情 | `/articles/:id` | 完整内容 + 核心要点 |
| 分享提交 | `/share/submit` | DeepSeek API AI提炼 → 编辑发布 |
| 分享广场 | `/share/square` | 社区分享内容展示 |
| 404 | 任意无效路由 | 禅意错误页面 |

## 🛠 技术栈

- Vue 3 + Composition API + `<script setup>`
- Vue Router (Hash 模式, GitHub Pages 兼容)
- Tailwind CSS (自定义米白大地色系)
- Vite 构建工具
- 纯静态部署 (GitHub Pages)

## 🚀 本地开发

```bash
npm install
npm run dev    # 开发服务器 http://localhost:5173
npm run build  # 构建到 dist/
```

## 📐 设计规范

- **色系**: #F5F0E8 (米白) / #D4C5A9 (大地) / #8B7355 (深褐) / #4A3728 (文字)
- **字体**: Noto Serif SC (衬线) + 系统默认
- **风格**: 极简禅意，圆角柔和，留白充足

## 🤖 LLM 提炼模块

分享提交页支持纯前端调用 DeepSeek API：
1. 用户输入心得 → 点击"AI提炼"
2. 在输入框中填入自己的 DeepSeek API Key
3. API Key 保存在 localStorage，不会上传服务器
4. 提炼结果可逐条编辑、增删 → 确认发布
