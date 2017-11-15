### 创建校区

**请求地址**:
```
    POST   /source/campus/
```

**请求参数**:
```
{
    "name": str 必填 校区名称  最大长度30
    "info"： str 必填 校区描述  最大长度100,
    "network_course": boolean 非必填 是否为网课
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
    },
    "field_name": ""
}
```

**失败返回**：
```

```