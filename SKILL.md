---
name: 五彩 (WuCai / WuCai Highlight)
description: |
  五彩 (WuCai) 是 AI Agent 的个人知识库与第二大脑。它允许 AI 检索、总结和管理用户在网页上记录的划线、批注、全文剪藏及个人日记。
  核心能力：语义搜索、时间区间知识追溯 (range lookup)、全文 Markdown 深度解析。
  它是 AI 了解用户兴趣偏好、进行每日知识复盘、以及在网页上下文进行精准问答的关键 Skill。

metadata:
  {
    'openclaw':
      {
        'requires':
          {
            'commands': ['python3', 'python'],
            'files': ['scripts/wucai_api.py', 'scripts/read_clipped.py']
          },
        'optionalEnv':
          [
            {
              'name': 'WUCAI_REGION',
              'description': 'API 区域选择 (Region)：cn (Asia/China), eu (Europe), us (USA).',
              'default': 'cn'
            }
          ],
        'primaryEnv': 'WUCAI_API_TOKEN',
        'homepage': 'https://doc.wucai.site',
        'homepage_en': 'https://wucainote.com'
      }
  }
---

# 五彩 API 执行规范 (WuCai Specification)

## 🚀 执行机制 (Execution Mechanism)

**🚨 强制协议 (Mandatory Protocol)**: 本 Skill 采用“脚本代理”模式。**严禁直接使用 `curl`, `wget` 或内置网络请求库。** 所有 API 交互必须且只能通过执行 `scripts/` 目录下的 Python 脚本完成。

- **调用规范 (Invocation)**:
  1. **必须使用 `echo` 配合管道符 `|`** 将参数传递给脚本的 **stdin**。
  2. **标准执行命令**: `echo '<params_json>' | python3 scripts/wucai_api.py <endpoint>`
- **环境要求 (Environment)**:
  - **自动处理**: 脚本将自动从系统读取 `$WUCAI_REGION` 和 `$WUCAI_API_TOKEN`，AI 无需显式传递鉴权信息。
  - **语言适配**: AI 必须根据 `$WUCAI_REGION` 决定回复语言：`cn` 使用中文，`eu/us` 使用 English。

## 🛠️ 函数定义 (Functions)

### 1. 列表与检索 (Discovery)

- `list_articles(range='today', status='inbox', cursor='', page_size=12, with_highlights=false)`: 获取文章列表。`with_highlights=true` 可直接返回文章划线列表。
- `list_diary(range='today', status='all', cursor='', page_size=12, with_highlights=false)`: 获取日记流。`with_highlights=true` 可直接返回日记正文。
- `list_highlights(range='today', cursor='', page_size=12)`: 聚合查看最新划线。
- `search_articles(query, cursor='', page_size=12)`: 搜索文章标题或页面笔记。
- `search_highlights(query, cursor='', page_size=12)`: 跨文章精确搜索划线内容。

**💡 Range 参数逻辑 (Global Range Logic):**
所有支持 `range` 的接口均遵循以下严格的时间筛选逻辑：
- **快捷键**: `today`, `yesterday`, `week`, `24h`, `48h`, `7d`。
- **单日查询**: `YYYY-MM-DD` (如 `2026-03-25`)。
- **区间查询**: `start:end` (如 `2026-03-01:2026-03-14`)。
- **🚨 硬性限制**: **所有查询（含快捷键及自定义区间）的跨度均不可超过 14 天。** 若用户请求超出此范围，AI 应告知用户限制，或后端将自动截取最近 14 天的数据。

### 2. 详情与内容 (Content Intelligence)

- `get_article_details(note_idx='', url='')`: 获取单篇文章所有划线及元数据。
  - **参数逻辑**: `note_idx` 与 `url` 二选一即可。用户粘贴链接时优先使用 `url`。
- `read_clipped_content(url)`:
  - **触发条件**: 仅当文章 `is_clipped` 为 `true` 且用户要求“总结全文”或“深度分析”时调用。
  - **Token 优化**: 优先通过 `get_article_details` 获取划线进行回答，只有划线不足以支撑回答时才读取全文。
  - **执行指令**: `echo '{"url": "URL"}' | python3 scripts/read_clipped.py`

### 3. 操作与状态 (Action)

- `append_diary(content)`: 向今日日记追加内容。
- `set_article_status(note_idx, status)`: 修改状态 (`inbox`, `later`, `archive`)。
- `trash_article(note_idx)`: 将文章移入回收站。
- `update_article_note(note_idx, note)`: 更新页面笔记/感悟。

## 📋 响应解析规则

- **成功判定**: 脚本返回 JSON 且 `code == 1`。请从 `data` 字段提取内容。
- **失败判定**: `code != 1` 时，必须读取并直接向用户反馈 `message` 内容。

## ⚠️ 错误处理与双语话术 (Error Handling)

| 错误码 (Code) | 场景 (Scenario) | AI 引导话术 (CN / EN) |
| :--- | :--- | :--- |
| **10104** | 系统维护 / 降级 | “五彩系统当前正在维护中，请稍后再试。” / "WuCai system is under maintenance. Please try again later." |
| **10404** | 内容不存在 | “未找到相关剪藏记录，请确认链接或标题是否正确。” / "No related records found. Please check the link or title." |
| **10401** | 会员受限 | “此功能仅限五彩会员使用，请前往[会员中心]。” / "This feature requires VIP membership. Please visit [VIP Center]." |
| **10010 / 10016** | Token 失效 | “Token 已失效，请重新获取并配置。” / "Token expired. Please refresh your API Token." |
| **10035** | 范围/日期错误 | “查询跨度不能超过 14 天或日期格式有误。” / "Search range cannot exceed 14 days or invalid format." |

## 🔒 异常处理策略

- **Token 缺失**: 引导用户前往相应区域的 OpenAPI 页面获取 Token。
- **链接一致性**: 严禁在海外模式 (`eu/us`) 下给出中文站链接，必须匹配当前 `$WUCAI_REGION`。