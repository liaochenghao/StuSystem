###    修改密码

**请求地址**:
```
    PUT     /admin/child_user/[user_id]/update_password/
```

**请求参数**:
```
    {
        "password": str 必填，最小长度6
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "密码修改成功",
    "data": {},
    "field_name": ""
}
```

**失败返回**：
```

```