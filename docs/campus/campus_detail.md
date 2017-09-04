### 获取校区详情


**请求地址**:
```
    GET   /course/campus/[campus_id]/
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
        "id": 12,
        "name": "测试校区",
        "info": "123456",
        "create_time": "2017-07-18T16:27:09Z",
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
    "field_name": ""
}
```

**失败返回**：
```

```