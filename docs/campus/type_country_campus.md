### 根据暑校类型获取对应国家，校区信息

**请求地址**:
```
    GET     /course/campus_type/type_country_campus/
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
    "data": [
        {
            "id": 1,
            "title": "北美暑校",
            "create_time": "2017-07-04T00:00:00Z",
            "campuscountry_set": [
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
                        {
                            "id": 2,
                            "name": "上海校区",
                            "campus_country": 1,
                            "info": "123",
                            "create_time": "2017-06-14T23:40:47Z"
                        },
                    ]
                },
                {
                    "id": 2,
                    "name": "美国",
                    "campus_type": 1,
                    "create_time": "2017-07-16T14:52:52Z",
                    "campus_set": [
                        {
                            "id": 5,
                            "name": "成都校区",
                            "campus_country": 2,
                            "info": "123",
                            "create_time": "2017-06-14T23:41:50Z"
                        },
                        {
                            "id": 6,
                            "name": "武汉校区",
                            "campus_country": 2,
                            "info": "123",
                            "create_time": "2017-06-14T23:42:18Z"
                        },
                    ]
                }
            ]
        },
    ],
    "field_name": ""
}
```

**失败返回**：
```

```