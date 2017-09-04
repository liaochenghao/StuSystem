### 创建暑校类型

**请求地址**:
```
    POST   /course/campus_type/
```

**请求参数**:
```
{
    "title": str  暑校类型  最大长度30,
    "campus_country": "" str 暑校国家
}
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