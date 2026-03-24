# 五彩 API 详细参考

## 目录

- [错误码表](#错误码表)
- [请求格式和返回格式详细说明](#请求格式和返回格式详细说明)
- [记笔记接口](#记笔记接口)

---

## 错误码表

| 错误码 | 说明 |
|------|------|
| 1     | 成功, success |
| 10010 | Token Expired |
| 10016 | Api Key error |
| 10017 | app secret error |
| 10401 | 仅会员可以，引导去开通会员 |

---

## 请求格式和返回格式详细说明
- api 会返回 JSON 格式
  - 返回的JSON里，code 等于数字 1 表示成功，其他值表示失败。 code 是错误码的意思。
  - 当结果失败时，message 字段会包含错误信息
  - data 字段会包含实际返回的数据，后面每个接口会具体说明data的返回格式。

比如，这个是成功的返回结果
```json
{
  "code": 1,
  "data": {
    "msg2": "read done. replyed: Gemini"
  },
  "message": "",
  "timestamp": 1774339535
}
```

这是一个失败的返回结果
```json
{
  "code": 10000,
  "data": null,
  "message": "No Auth",
  "timestamp": 1774339984
}
```

---

## 记笔记接口

接口: `POST /demo` 

请求体字段：
```json
{
  "msg1": "你好"
}
```

返回的data字段数据：
```json
{
  "msg2": "read done. replyed"
}
```

---
