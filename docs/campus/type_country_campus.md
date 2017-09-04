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
            "campus_country": {
                "key": "NORTH_AMERICA",
                "verbose": "北美暑校"
            },
            "campus_type": [
                {
                    "id": 1,
                    "title": "太阳系暑校",
                    "create_time": "2017-09-04T13:59:43Z",
                    "campus": [
                        {
                            "id": 1,
                            "name": "成都校区",
                            "info": "123",
                            "create_time": "2017-06-14T23:40:30Z"
                        },
                        {
                            "id": 6,
                            "name": "å—æ˜Œæ ¡åŒº",
                            "info": "123",
                            "create_time": "2017-06-14T23:42:18Z"
                        },
                        {
                            "id": 11,
                            "name": "åŒ—äº¬æ ¡åŒº",
                            "info": "65",
                            "create_time": "2017-07-17T15:35:43Z"
                        }
                    ]
                },
                {
                    "id": 2,
                    "title": "地球暑校",
                    "create_time": "2017-09-04T07:44:02Z",
                    "campus": [
                        {
                            "id": 2,
                            "name": "成都校区",
                            "info": "123",
                            "create_time": "2017-06-14T23:40:47Z"
                        },
                        {
                            "id": 7,
                            "name": "å¹¿å·žæ ¡åŒº",
                            "info": "123",
                            "create_time": "2017-06-14T23:42:45Z"
                        },
                        {
                            "id": 12,
                            "name": "åŒ—äº¬æ ¡åŒº",
                            "info": "45",
                            "create_time": "2017-07-17T15:36:27Z"
                        }
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