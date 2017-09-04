### 获取暑校类型详情


**请求地址**:
```
    GET   /course/campus_type/[campus_type_id]/
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
        "id": 4,
        "title": "非洲暑校",
        "create_time": "2017-07-13T15:43:52.714693Z",
        "campus_country":{
            "key": "NORTH_AMERICA",
            "verbose": "北美暑校"
        },
    },
    "field_name": ""
}
```

**失败返回**：
```

```