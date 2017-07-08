### 项目管理项目列表

**请求地址**:
```
    GET     /admin/project/
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
        "count": 3,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 2,
                "campus_name": "北京校区",
                "name": "北京校区一期项目",
                "applyed_num": 26,              申请人数
                "payed_num": 1                  缴费人数
            },
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```