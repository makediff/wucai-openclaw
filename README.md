# 五彩 Skill

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)

五彩 - 网页划线高亮批注和剪藏工具

---

## ✨ 核心能力

| 能力                         | 说明                                       |
| ---------------------------- | ------------------------------------------ |
| **写日记/daily/journal**     | 写下自己的生活、工作、学习等，方便后续查看 |
| **查看最近的 daily/日记**    | 查看最近的 daily/日记，方便查看            |
| **查看最近阅读的文章和划线** | 查看最近阅读的文章和划线，方便查看和管理   |
| **demo**                     | 用来测试五彩 demo                          |

---

## 💡 使用场景

### ✏️ 随手记录

**通勤路上想到一个点子**

> 👤 记一下：支付流程可以加一个进度条，用户等待时不焦虑
>
> 🤖 已记录，自动打上「产品优化」标签。

---

## 📦 安装

### 方式一：通过 ClawHub 安装（推荐）

```bash
clawhub install wucai
```

### 方式二：让 AI 助手安装

> 帮我安装 五彩 skill，地址是 https://raw.githubusercontent.com/makediff/wucai-openclaw/main/SKILL.md

### 方式三：手动安装

```bash
mkdir -p ~/.openclaw/workspace/skills/wucai
cd ~/.openclaw/workspace/skills/wucai
curl -sL https://raw.githubusercontent.com/makediff/wucai-openclaw/main/SKILL.md -o SKILL.md
curl -sL https://raw.githubusercontent.com/makediff/wucai-openclaw/main/package.json -o package.json
```

---

## 🔑 配置

### 通过后台复制五彩 API TOKEN

告诉 AI 助手：

> 帮我配置五彩
详细见 [SKILL.md](SKILL.md#连接五彩) 里的 连接五彩章节

---

## 🔐 安全说明

> ⚠️ **隐私保护**：笔记是你的私密数据，AI 会严格校验身份。

- 配置 `WUCAI_API_TOKEN` 后，只有你能操作笔记
- 群聊中其他人无法通过 AI 读取你的笔记
- **不要在聊天中发送 WUCAI_API_TOKEN**，请手动配置到环境变量

---

## 📜 相关链接

- [五彩官网](https://doc.wucai.site/about/wucai.html)
- [五彩官网 - 欧洲和美国区域](https://wucainote.com/about/wucai.html)
- [ClawHub](https://clawhub.ai/iswalle/wucai)
- [开通会员](https://marker.dotalk.cn/#/personSetting/membership)

---

## License

MIT-0 (MIT No Attribution) · Published on [ClawHub](https://clawhub.ai)
