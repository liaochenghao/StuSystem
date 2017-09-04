### 获取校区列表

**请求地址**:
```
    GET   /course/campus/
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
                "campus_type": {
                    "id": 1,
                    "title": "太阳系暑校",
                    "create_time": "2017-09-04T13:59:43Z",
                    "campus_country": {
                        "key": "NORTH_AMERICA",
                        "verbose": "北美暑校"
                    }
                }
            },
        ]
    "field_name": ""
}
```

**失败返回**：
```

```