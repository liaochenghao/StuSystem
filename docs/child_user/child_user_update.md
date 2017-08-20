###  子账号更新

**请求地址**:
```
    PUT/PATCH     /admin/child_user/[user_id]/
```

**请求参数**:
```
     {
        "name": str  姓名  必填
        "username": str  用户名  必填
        "is_active": boolean    是否启用  默认启用
        "role": str  角色  必填
    }
```

**成功返回**：
```
    {
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 32,
        "name": "张啦啦",
        "username": "zhanglala",
        "is_active": true,
        "qr_code": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQEJ8TwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyY1AxSnhBMEdjMGoxMDAwMGcwM2MAAgQupHxZAwQAAAAA",
        "role": {
            "key": "MARKET",
            "verbose": "市场部"
        }
    },
    "field_name": ""
}
```

**失败返回**：
```

```