[English](README.md)

# dev-skills（开发技能库）

一套可复用的 AI 编程 Agent 技能集，每个技能都是独立文件夹，包含指令、示例、脚本和模板。

## 技能列表

| 技能 | 说明 |
|---|---|
| `api-designer` | REST API 设计 — 路由、状态码、认证、版本管理 |
| `code-review` | 结构化代码审查 — 正确性、安全性、性能等多维度 |
| `db-schema` | PostgreSQL 数据库设计、索引、迁移、pgvector |
| `debug-assistant` | 系统化调试 — 报错分析、常见错误、根因定位 |
| `dockerfile` | 适用于各类技术栈的 Dockerfile 与 docker-compose |
| `git-workflow` | 提交信息、分支策略、PR、rebase、撤销操作 |
| `test-writer` | pytest 单元测试、fixture、mock、集成测试 |

## 目录结构

每个技能文件夹包含：
- `SKILL.md` — Agent 加载的主指令文件
- `examples.md` — 使用示例
- `scripts/` — 可运行脚本
- `template/` — 模板文件

## 同步地址

这些技能也内置于完整 Agent 项目中：[github.com/YSMsimon/this-is-my-agent](https://github.com/YSMsimon/this-is-my-agent/tree/master/skills)