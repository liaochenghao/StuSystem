### 获取用户信息

**请求地址**:
```
    GET     /auth/user/info/[user_id]/
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
            "id": 1,                            int     用户id
            "name": "yirantai",                 str     用户姓名
            "email": "896275756@qq.com",        str     email
            "wechat": "flyerweixin",            str     微信号
            "school": "",                       str     意向学校
            "wcampus": null                     str     意向校区
        },
        "field_name": ""
    }
```

**失败返回**：
```

```