### 获取暑校类型列表

**请求地址**:
```
    GET   /course/campus_type/
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
        "count": 3,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "title": "北美暑校",        str     暑校类型名称
                "create_time": "2017-06-14T23:38:14Z"
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```