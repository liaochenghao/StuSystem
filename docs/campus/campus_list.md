### 获取校区列表

**请求地址**:
```
    GET   /course/campus/
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
        "count": 10,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "北京校区",
                "campus_country": {
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
                        {
                            "id": 2,
                            "name": "上海校区",
                            "campus_country": 1,
                            "info": "123",
                            "create_time": "2017-06-14T23:40:47Z"
                        },
                        {
                            "id": 3,
                            "name": "南京校区",
                            "campus_country": 1,
                            "info": "123",
                            "create_time": "2017-06-14T23:41:05Z"
                        },
                        {
                            "id": 4,
                            "name": "长沙校区",
                            "campus_country": 1,
                            "info": "123",
                            "create_time": "2017-06-14T23:41:27Z"
                        },
                        {
                            "id": 9,
                            "name": "网课",
                            "campus_country": 1,
                            "info": "123",
                            "create_time": "2017-06-14T23:43:28Z"
                        }
                    ]
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