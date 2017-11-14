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

```
备注：管理后台测试账号：AdminUser, 密码：123456
     学生微信端调试账号：StudentTest, 密码：123456
```

**成功返回**：
```
{
  "code": 0,
  "msg": "登录成功",
  "data": {
    "user_id": 1,
    "ticket": "TK-VbT5EBfMGlFOCicKdDjo"
    "role": "ADMIN"
  },
  "field_name": ""
}
```

```
    role类型： ADMIN--管理员，STUDENT--学生，MARKET--市场人员，FINANCE--财务人员
```

**失败返回**：
```

```