# 五彩 (WuCai / WuCai Highlight) Skill for OpenClaw

[](https://opensource.org/licenses/MIT-0)

**五彩 (WuCai)** - 网页划线批注、全文剪藏与个人知识库管理工具。  
**WuCai Highlight** - Web highlighter, annotation, full-text clipping, and personal knowledge base manager.

-----

## ✨ 核心能力 (Core Capabilities)

| 能力 (Capability) | 对应函数 (Function) | 说明 (Description) |
| :--- | :--- | :--- |
| **📥 知识流管理** | `list_articles` | 分页浏览文章，支持 `inbox`, `later`, `archive` 状态流转。 |
| **🔍 全局深度搜索** | `search_articles`, `search_highlights` | **双索引搜索**：精准定位文章标题、笔记内容或划线文本。 |
| **✍️ 灵感随手记** | `append_diary`, `list_diary` | 快速向今日日记追加内容，或在 **14天跨度内** 回顾历史心路。 |
| **🔗 链接深度感知** | `get_article_details` | **URL 识别**：直接粘贴网址，AI 自动判断是否已剪藏并同步已有划线。 |
| **📝 笔记增强** | `update_article_note` | 随时为文章补充新的阅读评价、感悟或 AI 生成的摘要。 |

-----

## 🔑 配置指南 (Setup Guide)

### 1\. 获取 Token (Get Your Token)

**🚨 重要提示 (Important)**: 五彩采用 **数据分区隔离** 架构（CN/EU/US）。不同区域的账号数据完全独立且不互通。请根据您注册账号时选择的区域获取对应的 **OpenClaw Token**（以 `wct-` 开头）：

  - **中国/亚洲 (cn)**: [获取 Token](https://marker.dotalk.cn/#/personSetting/openapi)
  - **欧洲 (eu)**: [Get Token](https://eu.wucainote.com/#/personSetting/openapi)
  - **美国 (us)**: [Get Token](https://us.wucainote.com/#/personSetting/openapi)

### 2\. 在 AI 助手中配置 (Config in AI)

  - **连接 (Connect)**: 告诉 AI 助手 **“帮我配置五彩”** 或 **"Help me configure WuCai"**。
  - **设置 Token**: 将拷贝的 **OpenClaw Token** 粘贴给 AI 即可完成绑定。
  - **切换区域 (Switch Region)**: 默认区域为 `cn`。如果您在海外注册使用，请告知 AI：
    > *“设置五彩区域为 eu”* 或 *"Set WuCai region to us"*。  
    > **注意**：切换区域意味着 AI 将连接到不同的物理集群。各区域数据不互通，切换后将无法搜索到原区域的笔记。

-----

## 📦 安装 (Installation)

### 方式一：通过 ClawHub 安装 (Recommended)

```bash
clawhub install wucai
```

### 方式二：让 AI 助手直接安装 (Via AI Agent)

> 帮我安装五彩 Skill，地址是 `https://raw.githubusercontent.com/makediff/wucai-openclaw/main/SKILL.md`

-----

## 🔐 安全与隐私 (Security & Privacy)

  - **隐私隔离**: 笔记和日记是私密数据，AI 仅在您的明确指令下才会读取或搜索相关内容。
  - **数据跨度限制**: 为了性能与隐私平衡，单次时间范围查询（Range Query）最大跨度限制为 **14 天**。
  - **本地执行**: 所有 API 请求通过内置脚本 `scripts/wucai_api.py` 在本地执行，具备 15s 超时保护，确保数据链路安全稳定。

-----

## 📜 相关链接 (Links)

  - **Official Website**: [中文 (cn)](https://doc.wucai.site/) | [Global (eu/us)](https://wucainote.com/)
  - **Feedback**: [GitHub Issues](https://github.com/makediff/wucai-openclaw/issues)
  - **License**: MIT-0

-----

## License

MIT-0 (MIT No Attribution) · Published on [ClawHub](https://clawhub.ai)