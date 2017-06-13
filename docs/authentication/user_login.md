### 用户登录接口

**请求地址**:
```
    POST    /auth/user/login/
```

**请求参数**:
```
    {
        "username": ""     str   用户名    最小长度为6位，最大长度30位
        "password": ""     str   密码      最小长度为6位，最大长度30位
    }
```

**成功返回**：
```
{
  "code": 0,
  "msg": "登录成功",
  "data": {
    "user_id": 1,
    "ticket": "TK-VbT5EBfMGlFOCicKdDjo"
  },
  "field_name": ""
}
```

**失败返回**：
```

```