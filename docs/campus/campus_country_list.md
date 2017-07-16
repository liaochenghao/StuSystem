###   暑校国家列表

**请求地址**:
```
    GET     ／course/campus_country/
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
        "count": 4,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "加拿大",
                "campus_type": 1,
                "create_time": "2017-07-16T14:52:26Z"
            },
            {
                "id": 2,
                "name": "美国",
                "campus_type": 1,
                "create_time": "2017-07-16T14:52:52Z"
            },
            {
                "id": 3,
                "name": "澳大利亚",
                "campus_type": 2,
                "create_time": "2017-07-16T14:53:14Z"
            },
            {
                "id": 4,
                "name": "新西兰",
                "campus_type": 2,
                "create_time": "2017-07-16T14:53:22Z"
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```