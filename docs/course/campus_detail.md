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
        "id": 1,
        "name": "北京校区",
        "campus_type": {
            "id": 1,
            "title": "北美暑校",
            "create_time": "2017-06-14T23:38:14Z"
        },
        "info": "123",
        "create_time": "2017-06-14T23:40:30Z"
    },
    "field_name": ""
}
```

**失败返回**：
```

```