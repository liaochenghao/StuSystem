### 更新校区

**请求地址**:
```
    PUT/PATCH   /course/campus/[campus_id]/
```

**请求参数**:
```
{
    "campus_type": int   暑校类型id
    "name": str          校区名称
    "info": str          校区说明  最大长度100
}
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