### 获取暑校类型详情


**请求地址**:
```
    GET   /course/campus_type/[campus_type_id]/
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
        "id": 4,
        "title": "欧洲暑校",
        "create_time": "2017-06-19T14:34:32.826399Z"
        "campus_set": [
                    {
                        "id": 1,
                        "name": "北京校区",
                        "campus_type": 1,
                        "info": "123",
                        "create_time": "2017-06-14T23:40:30Z"
                    },
                ]
            },
    },
    "field_name": ""
}
```

**失败返回**：
```

```