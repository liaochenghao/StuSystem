### 获取校区列表

**请求地址**:
```
    GET     ／common/campus/
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
        "count": 9,                     int   总数
        "next": null,                   str   下一页地址
        "previous": null,               str   上一页地址
        "results": [
            {
                "id": 1,
                "campus_type": {                    #校区类型
                    "id": 1,
                    "title": "北美暑校",                         #  str   暑校类别名称
                    "create_time": "2017-06-14T23:38:14Z"       #  str   创建时间
                    },
                "name": "北京校区",                 str     校区名称
                "info": "123",                     str     校区描述
                "create_time": "2017-06-14T23:40:30Z"       # str 创建时间
            },
        ]
    },
"field_name": ""
}
```

**失败返回**：
```

```