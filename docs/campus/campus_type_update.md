### 更新暑校类型

**请求地址**:
```
    PUT/PATCH   /course/campus_type/[campus_type_id]/
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
        "title": "欧洲暑校",
        "create_time": "2017-06-19T14:34:32.826399Z"
    },
    "field_name": ""
}
```

**失败返回**：
```

```