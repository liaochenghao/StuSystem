###  更新暑校国家

**请求地址**:
```
    PUT/PATCH       /course/campus_country/
```

**请求参数**:
```
    {
        "name": str   必填  国家名称    最大长度30，
        "campus_type": int 必填   暑校类型
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 1,
        "name": "加拿大",
        "campus_type": 1,
        "create_time": "2017-07-16T14:52:26Z"
    },
    "field_name": ""
}
```

**失败返回**：
```

```