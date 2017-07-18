### 创建校区

**请求地址**:
```
    POST   /course/campus/
```

**请求参数**:
```
{
    "name": str  校区名称  最大长度30
    "campus_country": list   暑校国家类型id的list
    "info"： str  校区描述  最大长度100
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 12,
        "name": "测试校区",
        "info": "123456",
        "create_time": "2017-07-18T16:27:08.808114Z",
        "campus_country": [
            {
                "id": 1,
                "name": "加拿大1",
                "campus_type": 1,
                "create_time": "2017-07-16T14:52:26Z"
            },
            {
                "id": 2,
                "name": "美国",
                "campus_type": 1,
                "create_time": "2017-07-16T14:52:52Z"
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```