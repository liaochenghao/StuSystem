### 已发送好友申请

**请求地址**:
```
    POST     /auth／user/[user_id]/sales_man/
```

**请求参数**:
```
   {
       "sales_man": int     销售顾问id
   }
```

**成功返回**：
```
{
  "code": 0,
  "msg": "操作成功",
  "data": {},
  "field_name": ""
}
```

**失败返回**：
```
{
  "code": 400,
  "msg": "已有关联的销售顾问",
  "data": {},
  "field_name": "non_field_errors"
}
```