### 销售顾问二维码

**请求地址**:
```
    GET     /auth／user/[user_id]/sales_man/
```

**请求参数**:
```
    无
```

**成功返回**：
```
{
  "code": 0,
  "msg": "请求成功",
  "data": {
    "id": 3,
    "name": "wangwu",               str  销售顾问名称
    "email": "784512584@qq.com",    str  联系邮箱
    "qr_code": "http://www.qq.com"  str  二维码地址
  },
  "field_name": ""
}
```

**失败返回**：
```
{
  "code": 0,
  "msg": "请求成功",
  "data": {}
  "field_name": ""
}

```