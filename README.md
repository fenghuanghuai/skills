# Claude Skills Collection

<div align="center">

![Claude Skills](https://img.shields.io/badge/Claude-Skills-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Skills](https://img.shields.io/badge/skills-2-orange?style=for-the-badge)

**个人 Claude Code 技能集合**

扩展 Claude AI 能力的自定义技能包

[快速开始](#-快速开始) • [技能列表](#-技能列表) • [项目结构](#-项目结构) • [使用示例](#-使用示例)

</div>

---

## 📖 简介

这个仓库收集了我为 Claude Code 开发的自定义技能（Skills），用于扩展 AI 的专业能力和工作流集成。

每个技能都是经过精心设计和测试的独立模块，包含完整的源码、文档和示例。

---

## 🎯 技能列表

### OpenCode Service

> OpenCode CLI 集成指南

**功能特性：**
- 🤖 AI 代码审查集成到 CI/CD 流水线
- 📝 创建用于代码分析的 Makefile 目标
- 🔍 自动化代码质量检查
- 📚 OpenCode CLI 使用模式参考

**适用场景：**
- DevOps 自动化
- 代码质量门禁
- CI/CD 管道集成
- 本地开发工作流

**源码目录：** [`opencode-service/`](./opencode-service/)
**打包文件：** [`opencode-service.skill`](./opencode-service.skill) (9 KB)

---

### SMTP Email

> 通过 SMTP 协议发送邮件

**功能特性：**
- 📧 程序化邮件发送
- 📎 支持附件
- 🔐 环境变量配置
- 👥 白名单发件人控制
- 📬 邮件监听和自动回复

**适用场景：**
- 发送通知和警报
- 报告和数据导出
- 自动化邮件任务
- 邮件驱动的自动化工作流

**源码目录：** [`smtp-email/`](./smtp-email/)
**打包文件：** [`smtp-email.skill`](./smtp-email.skill) (9 KB)

---

## 🚀 快速开始

### 方式一：直接使用 .skill 文件

下载 `.skill` 文件并放置到 Claude skills 目录：

```bash
# 下载
wget https://raw.githubusercontent.com/fenghuanghuai/skills/main/opencode-service.skill
wget https://raw.githubusercontent.com/fenghuanghuai/skills/main/smtp-email.skill

# 安装
cp *.skill ~/.claude/skills/
```

### 方式二：从源码构建

克隆仓库并自行打包：

```bash
git clone https://github.com/fenghuanghuai/skills.git
cd skills

# 使用 skill-creator 打包（需要安装）
python3 /path/to/skill-creator/scripts/package_skill.py opencode-service
python3 /path/to/skill-creator/scripts/package_skill.py smtp-email
```

---

## 📁 项目结构

```
skills/
├── README.md
├── opencode-service.skill          # 打包文件
├── smtp-email.skill                # 打包文件
├── opencode-service/               # 源码目录
│   ├── SKILL.md
│   └── references/
│       ├── cli-reference.md
│       ├── integration-patterns.md
│       └── troubleshooting.md
└── smtp-email/                     # 源码目录
    ├── SKILL.md
    ├── .gitignore
    └── scripts/
        ├── send_email.py
        ├── email_monitor.py
        ├── config.py
        └── config.example.py
```

---

## 📚 使用示例

### OpenCode Service

```bash
# 查看 CLI 命令参考
opencode --help

# 运行代码审查
opencode run "Review the code in src/"

# 启动服务模式
opencode serve --port 4096
```

### SMTP Email

```bash
cd smtp-email/scripts

# 配置邮件凭据
cp config.example.py config.py
# 编辑 config.py 填入您的 SMTP 信息

# 发送邮件
python3 send_email.py "recipient@example.com" "Hello" "This is a test"

# 启动邮件监听
python3 email_monitor.py
```

---

## 🔧 配置说明

### SMTP Email 配置

编辑 `smtp-email/scripts/config.py`：

| 变量 | 说明 | 示例 |
|------|------|------|
| `SMTP_SERVER` | SMTP 服务器地址 | `smtp.example.com` |
| `SMTP_PORT` | SMTP 端口 | `465` |
| `SMTP_USER` | SMTP 用户名 | `user@example.com` |
| `SMTP_PASSWORD` | SMTP 密码 | `your-password` |
| `SMTP_FROM` | 发件人邮箱 | `sender@example.com` |
| `IMAP_SERVER` | IMAP 服务器（监听用） | `imap.example.com` |
| `ALLOWED_SENDERS` | 允许的发件人列表 | `["a@q.com", "b@q.com"]` |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingSkill`)
3. 提交更改 (`git commit -m 'Add some AmazingSkill'`)
4. 推送到分支 (`git push origin feature/AmazingSkill`)
5. 开启 Pull Request

---

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE)

---

## 🔗 相关链接

- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [Skill 创建指南](https://github.com/anthropics/anthropic-agent-skills)
- [OpenCode 官方文档](https://opencode.ai)

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️**

Made with ❤️ by [fengguanghuai](https://github.com/fengguanghuai)

</div>
