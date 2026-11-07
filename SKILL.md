---
name: 五彩 (WuCai / WuCai Highlight)
description: |
  五彩 (WuCai) 是 AI Agent 的个人知识库与第二大脑。它允许 AI 检索、总结和管理用户在网页上记录的划线、批注、全文剪藏及个人日记。
  核心能力：跨区域语义搜索、时间区间知识追溯 (range lookup)、以及基于划线的精准内容问答。
  它是 AI 了解用户兴趣偏好、进行每日知识复盘、以及在网页上下文进行精准问答的关键 Skill。

metadata:
  {
    'openclaw':
      {
        'requires':
          {
            'commands': ['python3', 'python'],
            'files': ['scripts/wucai_api.py', 'cli/wucai_cli.py']
          },
        'optionalEnv':
          [
            {
              'name': 'WUCAI_REGION',
              'description': 'API 区域选择 (Region)：cn (Asia/China), eu (Europe), us (USA). ⚠️ 注意：各区域数据物理隔离。',
              'default': 'cn'
            }
          ],
        'primaryEnv': 'WUCAI_API_TOKEN',
        'homepage': 'https://wucainote.com/docs/',
        'homepage_en': 'https://wucainote.com'
      }
  }
---

# 五彩 API 执行规范 (WuCai Specification)

## 🚀 执行机制 (Execution Mechanism)

**🚨 强制协议 (Mandatory Protocol)**: 本 Skill 采用"脚本代理"模式。**严禁直接使用 `curl`, `wget` 或内置网络请求库。** 所有 API 交互必须且只能通过以下两种方式之一完成：

### 方式一：脚本调用 (推荐)

- **调用规范 (Invocation)**:
  1. **必须使用 `echo` 配合管道符 `|`** 将参数传递给脚本的 **stdin**。
  2. **标准执行命令**: `echo '<params_json>' | python3 scripts/wucai_api.py <endpoint>`
- **环境要求 (Environment)**:
  - **自动处理**: 脚本将自动从系统读取 `$WUCAI_REGION` 和 `$WUCAI_API_TOKEN`。
  - **数据隔离**: AI 必须意识到切换区域将连接到完全独立的数据库集群。
  - **语言适配**: AI 必须根据 `$WUCAI_REGION` 决定回复语言：`cn` 使用中文，`eu/us` 使用 English。
  - **超时保护**: 每个请求具备 **15s 超时**，超时后返回网络错误。

### 方式二：CLI 工具 (可选)

也可使用 `python3 cli/wucai_cli.py <subcommand>` 调用，CLI 提供更友好的子命令和参数解析。

```bash
python3 cli/wucai_cli.py list-highlights --range today --output json
python3 cli/wucai_cli.py search-highlights --query "machine learning" --output pretty
```

CLI 支持 `-o / --output` 选项：`json`（紧凑）、`pretty`（缩进）、`text`（人类可读）。

### 区域对照表

| 区域 (Region) | 域名 (Domain) | 获取 Token 页面 |
| :--- | :--- | :--- |
| **cn** | `marker.dotalk.cn` | [点击获取](https://marker.dotalk.cn/#/personSetting/openapi) |
| **eu** | `eu.wucainote.com` | [点击获取](https://eu.wucainote.com/#/personSetting/openapi) |
| **us** | `us.wucainote.com` | [点击获取](https://us.wucainote.com/#/personSetting/openapi) |

## 🛠️ 函数定义 (Functions)

### 1. 列表与检索 (Discovery)

- `list_articles(range='today', status='inbox', cursor='', page_size=12, with_highlights=false)`: 获取文章列表。`with_highlights=true` 可直接返回文章划线列表。
- `list_diary(range='today', status='all', cursor='', page_size=12, with_highlights=false)`: 获取日记流。`with_highlights=true` 可直接返回日记正文。
- `list_highlights(range='today', cursor='', page_size=12, type=0)`: 聚合查看最新划线。`type`: 0=全部, 1=文章(Article), 3=日记(Daily)。
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
  - **知识获取**: 建议在回答用户关于特定网页的问题前，先调用此函数获取已有划线和笔记。

### 3. 操作与状态 (Action)

- `append_diary(content)`: 向今日日记追加内容。
- `set_article_status(note_idx, status)`: 修改状态 (`inbox`, `later`, `archive`)。
- `trash_article(note_idx)`: 将文章移入回收站。
- `update_article_note(note_idx, note)`: 更新页面笔记/感悟。

## 📦 数据模型 (Data Models)

### ArticleDTO (文章/日记对象)

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `note_idx` | string | 唯一标识 ID |
| `note_type` | int | **0/1**: 文章 (Article); **3**: 日记 (Diary) |
| `page_title` | string | 页面标题 |
| `page_url` | string | 原始网页链接 |
| `page_note` | string | 用户对该页面的整体评价/笔记 |
| `highlight_count` | int | 划线总数 |
| `is_clipped` | bool | 是否为全文剪藏 |
| `highlights` | HighlightDTO[] | 当 `with_highlights=true` 时包含划线内容 |
| `tags` | string | 标签（逗号分隔） |

### HighlightDTO (划线对象)

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `h_id` | int64 | 划线唯一 ID |
| `content` | string | 网页高亮的原始文本 |
| `annotation` | string | 用户对该划线的批注/想法 |
| `image_url` | string | 关联的图片链接 |
| `tags` | string | 标签（逗号分隔） |

## 📋 响应解析规则

- **成功判定**: 脚本返回 JSON 且 `code == 1`。请从 `data` 字段提取内容。
- **失败判定**: `code != 1` 时，必须读取并直接向用户反馈 `message` 内容。
- **分页**: 列表接口返回的 `data` 中包含 `next_cursor` 字段。若 `next_cursor` 非空，说明还有更多内容，将其填入下一次请求的 `cursor` 参数即可继续翻页。

## ⚠️ 错误处理与双语话术 (Error Handling)

| 错误码 (Code) | 场景 (Scenario) | AI 引导话术 (CN / EN) |
| :--- | :--- | :--- |
| **-1** | 网络错误/服务端异常 | "网络连接失败或服务器异常，请稍后重试。" / "Network or server error. Please retry." |
| **10000** | 业务通用异常 | 直接展示返回的 `message` 内容。 |
| **10010 / 10016** | Token 缺失/失效 | "Token 已失效或无效，请重新获取并配置。" / "Token expired or invalid. Please refresh your API Token." |
| **10035** | 范围/日期错误 | "查询跨度不能超过 14 天或日期格式有误。" / "Search range cannot exceed 14 days or invalid format." |
| **10104** | 系统维护 / 降级 | "五彩系统当前正在维护或处于降级模式，请稍后再试。" / "WuCai system is under maintenance." |
| **10401** | 会员受限 | "此功能仅限五彩会员使用，请前往[会员中心]。" / "This feature requires VIP membership." |
| **10404** | 内容不存在 | "未找到相关记录。请检查链接或区域 ($WUCAI_REGION) 是否正确。" / "No records found. Please check URL or Region." |

## 💡 使用示例 (Examples)

### 脚本调用方式

```bash
# 查看今日划线
echo '{"range":"today","page_size":12}' | python3 scripts/wucai_api.py list_highlights

# 搜索划线内容
echo '{"query":"machine learning","page_size":12}' | python3 scripts/wucai_api.py search_highlights

# 获取文章详情（通过 URL）
echo '{"url":"https://example.com/article"}' | python3 scripts/wucai_api.py get_article_details

# 追加日记
echo '{"content":"今天学到了 AI Agent 的新模式"}' | python3 scripts/wucai_api.py append_diary
```

### CLI 调用方式

```bash
# 查看今日划线（json 输出）
python3 cli/wucai_cli.py list-highlights --range today -o json

# 查看本周文章（带高亮，缩进输出）
python3 cli/wucai_cli.py list-articles --range week --with-highlights -o pretty

# 搜索划线
python3 cli/wucai_cli.py search-highlights --query "machine learning"

# 追加日记
python3 cli/wucai_cli.py append-diary --content "今天学到了新东西"
```

### 响应结构示例 (成功)

```json
{
  "code": 1,
  "data": {
    "highlights": [
      {
        "h_id": 123456,
        "content": "高亮文本内容",
        "annotation": "用户批注",
        "image_url": "",
        "tags": "",
        "created_at": 1700000000
      }
    ],
    "next_cursor": "eyJwIjoyfQ=="
  },
  "message": "",
  "timestamp": 1700000000
}
```

## 🔒 异常处理策略

- **Token 缺失**: 引导用户前往相应区域的 OpenAPI 页面获取 Token。
- **链接一致性**: 严禁在海外模式 (`eu/us`) 下给出中文站链接，必须匹配当前 `$WUCAI_REGION`。
