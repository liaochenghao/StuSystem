### 子账号列表

**请求地址**:
```
    GET     /admin/child_user/
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
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": null,
                "username": "AdminUser",
                "is_active": true,
                "qr_code": null,
                "role": {
                    "key": "ADMIN",
                    "verbose": "管理员"
                }
            },
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```