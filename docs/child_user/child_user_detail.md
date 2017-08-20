###  子账号详情

**请求地址**:
```
    GET   /admin/user/[user_id]/
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