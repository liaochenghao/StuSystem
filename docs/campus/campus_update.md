### 更新校区

**请求地址**:
```
    PUT/PATCH   /course/campus/[campus_id]/
```

**请求参数**:
```
{
    "campus_type": int   暑校国家id
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
                "campus_type": 1,
                "create_time": "2017-07-16T14:52:26Z",
                "campus_set": [
                    {
                        "id": 1,
                        "name": "北京校区",
                        "campus_country": 1,
                        "info": "123",
                        "create_time": "2017-06-14T23:40:30Z"
                    },
                ]
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