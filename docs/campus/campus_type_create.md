### 创建暑校类型

**请求地址**:
```
    POST   /course/campus_type/
```

**请求参数**:
```
{
    "title": str  暑校类型  最大长度30
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
        "campus_set": []
    },
    "field_name": ""
}
```

**失败返回**：
```

```