###  是否需要完善档案信息

**请求地址**:
```
    GET     /auth/user/info/complete_personal_file/
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
        "need_complete_personal_file": boolean  True代表需要完善，False代表不需要完善
    },
    "field_name": ""
}
```

**失败返回**：
```

```