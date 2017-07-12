###    获取销售顾问列表

**请求地址**:
```
    GET     /admin/sales_man/
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
        "count": 4,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "zhangsan",
                "wechat": "xiubweixin",
                "email": "896254545@qq.com",
                "qr_code": "http://127.0.0.1:8002/media/http%3A/www.baidu.com"
            },
        ]
    },
    "field_name": ""
}

```

**失败返回**：
```

```