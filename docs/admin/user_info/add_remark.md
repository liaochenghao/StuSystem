###   添加学生备注

**请求地址**:
```
    POST    /admin/user_info/[user_id]/add_remark/
```

**请求参数**:
```
{
    "remark": 备注值，str   最大长度255
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 5,
        "remark": "you are my sunshine",
        "create_time": "2017-07-07T15:34:54.836714Z"
    },
    "field_name": ""
}
```

**失败返回**：
```

```