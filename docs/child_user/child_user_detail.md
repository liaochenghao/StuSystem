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
        "id": 1925,
        "name": "HD",
        "username": "HDeducation",
        "is_active": true,
        "qr_code": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQGI8TwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyVGJXTDhydzZlODMxMDAwMGcwM1kAAgRbpLRaAwQAAAAA",
        "role": {
            "key": "MARKET",
            "verbose": "市场部"
        },
        "bind_sales_man": null,
        "channel_id": 34
    },
    "field_name": ""
}
```

**失败返回**：
```

```