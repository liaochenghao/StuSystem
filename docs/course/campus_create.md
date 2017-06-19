### 创建校区

**请求地址**:
```
    POST   /course/campus/
```

**请求参数**:
```
{
    "name": str  校区名称  最大长度30
    "campus_type": int   暑校类型id
    "info"： str  校区描述  最大长度100
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 10,
        "name": "云南校区",           校区名称
        "campus_type": {             校区类型信息
            "id": 2,
            "title": "澳洲暑校",
            "create_time": "2017-06-14T23:38:18Z"
        },
        "info": "人见人爱，花见花开",  校区描述
        "create_time": "2017-06-19T14:58:34.083759Z"
    },
    "field_name": ""
}
```

**失败返回**：
```

```