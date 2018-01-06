### 小程序获取认证

**请求地址**:
```
    GET     /auth/user/authorize/
```

**请求参数**:
```
{
    "code":  str  跳转小程序成功后返回的code  必填
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "user_id": 2,
        "ticket": "TK-cYjGLohIRz2lCNSdtrQ8"
    },
    "field_name": ""
}
```

**失败返回**：
```

```