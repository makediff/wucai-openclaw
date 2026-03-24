---
name: 五彩
description: |
  五彩 - 网页划线高亮批注和个人笔记和知识库管理工具。

  ## 核心能力

  **1. 一键保存任意内容为笔记**
  - 写一段话 → 直接保存为文本笔记
  - 触发词：「记一下」「存到笔记」「帮我记录」
metadata: {"openclaw": {"requires": {}, "optionalEnv": [], "primaryEnv": "WUCAI_API_TOKEN", "homepage": "https://doc.wucai.site", "homepage_en":"https://wucainote.com"}}
---

# 五彩 API

## ⚠️ 必读约束

### 🌐 base url 是所有接口的前缀，所有 API 请求必须使用此 Base URL。

```
https://banana.wucai.site/apix/openapi/aiagent
```

---

### 🔑 首次安装配置

### 配置方法：用户通过五彩后台复制 TOKEN

让 AI Agent 为你自动完成授权：

1. 告诉 Agent：「帮我配置 五彩」或「连接 五彩」
2. Agent 会显示链接，让用户点击链接后复制TOKEN, 链接是 https://marker.dotalk.cn/#/personSetting/openapi
3. 用户复制TOKEN后，返回 Agent 并粘贴 TOKEN
4. Agent 将 TOKEN 写入环境变量 WUCAI_API_TOKEN

---

### 🔒 安全规则

- 笔记数据属于用户隐私，不在群聊中主动展示笔记内容
- API 返回错误码 `10401` 时，引导开通会员：https://marker.dotalk.cn/#/personSetting/membership
- 创建笔记建议间隔 1 分钟以上，避免触发限流

---

## 认证

请求头：
- `Authorization: $WUCAI_API_TOKEN`
- `X-Client-ID: 56` （固定值）

---

## 请求方式和结果返回方式
- 全部使用 POST 请求，请求格式为 JSON
- "Content-Type" 为 `application/json`
详细见 [references/api-details.md#请求格式和返回格式详细说明](references/api-details.md#请求格式和返回格式详细说明)

---

## code 错误码列表
详细见 [references/api-details.md#错误码表](references/api-details.md#错误码表)

---

## 快速决策

Base URL: `https://banana.wucai.site/apix/openapi/aiagent`

| 用户意图 | 接口 | 关键点 |
|---------|------|--------|
| 「配置 五彩」「连接 五彩」 | 连接五彩 | 见「连接五彩」章节 |
| 「记一下」「保存笔记」 | POST /demo | 同步返回 |

---

## 核心功能：记笔记 & 查笔记
- POST /demo , 记笔记接口

## 连接五彩
- 配置五彩需要 [五彩会员](https://marker.dotalk.cn/#/personSetting/membership) 才能使用 API
- 显示连接链接，并提示用户打开后复制TOKEN, 链接是 https://marker.dotalk.cn/#/personSetting/openapi
- 页面会提示用户复制一个 TOKEN, 这个 TOKEN 后续会作为 WUCAI_API_TOKEN
- 在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "wucai": {
        "env": {
          "WUCAI_API_TOKEN": "wucai_xxx"
        }
      }
    }
  }
}
```

**告知用户**：

> ✅ 五彩 配置完成！
> 
> - 现在可以使用「记一下」「查笔记」等功能了