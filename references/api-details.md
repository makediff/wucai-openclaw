# 五彩 API 详细参考 (WuCai API Reference)

## 1. 区域引导信息参考表 (⚠️ 必须严格匹配 $WUCAI_REGION)
AI 在引导用户配置时，必须根据当前区域环境变量动态生成链接，不得混用：

| 区域 (Region) | 前缀域名 (Domain) | 获取 Token 页面 (OpenAPI Page) |
| :--- | :--- | :--- |
| **cn** | `marker.dotalk.cn` | [点击获取](https://marker.dotalk.cn/#/personSetting/openapi) |
| **eu** | `eu.wucainote.com` | [点击获取](https://eu.wucainote.com/#/personSetting/openapi) |
| **us** | `us.wucainote.com` | [点击获取](https://us.wucainote.com/#/personSetting/openapi) |

---

## 2. 交互协议与响应规范 (Protocol & Response)

### 通用请求头 (Common Headers)
- `Authorization`: 用户的 API Token (以 `wct-` 开头)。
- `X-Client-ID`: `56` (固定值)。

### ⚠️ 响应解析准则 (Response Parsing Rules)
所有接口统一返回以下 JSON 结构，AI 必须严格执行判断：
1. **成功判定**: **仅当 `code` 等于数字 `1` 时**，视为请求成功。此时读取 `data` 字段。
2. **失败判定**: 当 `code` **不等于 `1`** 时，视为请求失败。此时 `data` 通常为 `null`，AI 必须读取 `message` 字段并向用户反馈原因。

#### 响应 JSON 结构：
- `code`: (int64) **唯一成功标识为 1**。
- `data`: (object|array|null) 实际业务数据。
- `message`: (string) 失败时的描述信息或引导话术。
- `timestamp`: (int64) 服务器当前时间戳。

---

## 3. 核心数据模型 (Data Models / DTOs)

### ArticleDTO (文章/日记对象)
当调用 `list_articles`, `list_diary`, `search_articles` 或 `get_article_details` 时返回。
- `note_idx`: (string) 唯一标识 ID。
- `note_type`: (int64) **0/1**: 文章 (Article); **3**: 日记 (Daily/Diary)。
- `page_title`: (string) 页面标题。
- `page_url`: (string) 原始网页链接。
- `page_note`: (string) 用户对该页面的整体评价/笔记。
- `highlight_count`: (int64) 划线总数。
- `is_clipped`: (bool) **关键标识**: 若为 `true`，代表服务器存有全文剪藏，AI 可引导用户读取 Markdown 原文。
- `highlights`: (HighlightDTO[]) 该文章下的划线列表。
- `tags`: (string) 标签（逗号分隔）。

### HighlightDTO (划线对象)
- `h_id`: (int64) 划线唯一 ID。
- `content`: (string) 网页高亮的原始文本。
- `annonation`: (string) 用户对该划线的批注（想法）。
- `image_url`: (string) 关联的图片链接。
- `tags`: (string) 标签（逗号分隔）。

---

## 4. 错误处理与双语话术 (Error Handling)

当插件返回特定的错误码时，AI 助手应根据以下话术进行引导：

| 错误码 (Code) | 场景 (Scenario) | AI 引导话术 (CN / EN) |
| :--- | :--- | :--- |
| **10104** | **系统维护 / 降级** | “五彩系统当前正在维护或处于降级模式，请稍后再试。” / "WuCai system is currently under maintenance or in degraded mode. Please try again later." |
| **10401** | 会员受限 | “此功能仅限五彩会员使用，请前往[会员中心]。” / "This feature requires VIP membership. Please visit [VIP Center]." |
| **10010 / 10016** | Token 失效 | “Token 已失效，请重新获取并配置。” / "Token expired. Please refresh your API Token." |
| **10000** | 业务通用异常 | 直接展示返回的 `message` 内容。 / Display the `message` content directly. |

---

## 5. 翻页与性能约束 (Pagination & Performance)
- **游标翻页**: 列表接口返回 `next_cursor`。若用户请求更多内容，将该值填入下一次请求的 `cursor` 字段中。
- **速率限制**: 写入操作（如 `append_diary`）建议间隔 1 分钟，批量拉取建议 `page_size` 设置在 12-30 之间。