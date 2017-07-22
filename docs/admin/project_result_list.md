### 所有学生学分转换列表

**请求地址**:
```
    GET     /admin/project_result/
```

**请求参数**:
```

```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 4,
                "project": {
                    "id": 2,
                    "campus_name": "北京校区",
                    "name": "北京校区一期项目"
                },
                "post_date": null,
                "post_channel": null,
                "post_number": null,
                "status": null,
                "img": null,
                "user_info": {
                    "id": 1,
                    "name": "zxc",
                    "email": "xcz1899@163.com",
                    "wechat": "34343"
                }
            },
    },
    "field_name": ""
}
```

**失败返回**：
```

```