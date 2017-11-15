### 更新校区

**请求地址**:
```
    PUT/PATCH   /source/campus/[campus_id]/
```

**请求参数**:
```
{
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
        "id": 10,
        "name": "云南校区",           校区名称
        "campus_country":
            {
                "id": 1,
                "name": "加拿大",
                "create_time": "2017-07-16T14:52:26Z",
            }
        "info": "人见人爱，花见花开",  校区描述
        "create_time": "2017-06-19T14:58:34.083759Z"
    },
    "field_name": ""
}
```

**失败返回**：
```

```