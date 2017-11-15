### 获取校区列表

**请求地址**:
```
    GET   /source/campus/
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
        "count": 10,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "北京校区",
                "info": "23456",
                "create_time": "2017-06-14T23:40:30Z",
            },
        ]
    "field_name": ""
}
```

**失败返回**：
```

```