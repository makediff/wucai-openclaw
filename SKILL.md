---
name: 五彩 (WuCai / WuCai Highlight)
description: |
  管理网页划线、批注、全文剪藏和日记。
  集成多区域 (CN/EU/US) 自动切换、15s 超时保护及中英文双语交互。

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
  1. **必须使用 `echo` 配合管道符 `|`** 将参数传递给脚本的 **stdin**，以规避 Shell 引号冲突与特殊字符解析错误。
  2. **标准执行命令**: `echo '<params_json>' | python3 scripts/wucai_api.py <endpoint>`
  3. **示例 (list_articles)**: `echo '{"range": "today"}' | python3 scripts/wucai_api.py list_articles`
- **环境要求 (Environment)**:
  - **脚本依赖**: 确保 `scripts/wucai_api.py` 和 `scripts/read_clipped.py` 位于正确路径。
  - **自动处理**: 脚本将自动从系统读取 `$WUCAI_REGION` 和 `$WUCAI_API_TOKEN`，AI 无需在 JSON 参数中包含这些信息。
  - **语言适配**: AI 必须根据 `$WUCAI_REGION` 决定回复语言：`cn` 使用中文，`eu/us` 使用 English。

## 🛠️ 函数定义 (Functions)

### 1. 列表与检索 (Discovery)

- `list_articles(range='today', status='inbox', cursor='', page_size=12, with_highlights=false)`: 获取文章。`range` 可选: `today`/`48h`/`week`/`all`。
- `list_diary(range='today', status='all', cursor='', page_size=12, with_highlights=false)`: 获取日记流。`with_highlights=true` 可在返回文章的同时直接包含对应的划线/日记内容。
- `list_highlights(range='today', cursor='', page_size=12)`: 聚合查看最新划线。
- `search_articles(query, cursor='', page_size=12)`: 搜索文章标题或笔记。
- `search_highlights(query, cursor='', page_size=12)`: 跨文章搜索划线内容。

### 2. 详情与内容 (Content Intelligence)

- `get_article_details(note_idx='', url='')`: 获取单篇文章所有划线及元数据。
- `read_clipped_content(clipp_url)`:
  - **触发条件**: 当文章 `is_clipped` 为 `true` 时，调用此函数读取 Markdown 全文进行摘要。
  - **执行指令**: `echo '{"url": "ARTICLE_URL"}' | python3 scripts/read_clipped.py`

### 3. 操作与状态 (Action)

- `append_diary(content)`: 向今日日记追加内容。
- `set_article_status(note_idx, status)`: 修改状态 (`inbox`, `later`, `archive`)。
- `trash_article(note_idx)`: 将文章移入回收站。
- `update_article_note(note_idx, note)`: 更新页面笔记/感悟。

## 📋 响应解析规则

- **成功判定**: 脚本返回 JSON 且 `code == 1`。请提取并处理 `data` 字段。
- **失败判定**: `code != 1` 时，必须读取 `message` 并直接反馈给用户。

## ⚠️ 动态引导约束 (Dynamic Guidance)

- **链接一致性**: 引导用户获取 Token 时，必须匹配当前 `$WUCAI_REGION`。
- **强制检查**: 输出链接前，必须查阅 `api-details.md` 获取对应区域的 OpenAPI 页面地址。**严禁**在海外模式下给出中文站链接。

## 🔒 异常处理

- **Code 10401**: 权限受限，根据区域引导至对应的会员中心。
- **Token 缺失**: 引导用户前往相应区域的 **OpenAPI 页面** 拷贝 OpenClaw Token。
