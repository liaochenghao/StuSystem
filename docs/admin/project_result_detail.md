### 某一学生学分转换详情

**请求地址**:
```
    GET     /admin/project_result/[user_id]/
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
        "id": 4,
        "project":{
        "id": 4,
        "project": {
            "id": 2,
            "campus_name": "北京校区",
            "name": "北京校区一期项目"
        },
        "post_datetime": null,          快递日期
        "post_channel": null,       快递方式
        "post_number": null,        快递单号
        "status": null,             状态值
        "img": null,                学分转换图片
        "user_info": {              用户信息
            "id": 1,
            "name": "zxc",
            "email": "xcz1899@163.com",
            "wechat": "34343"
        }
    },
    "field_name": ""
}
```

**失败返回**：
```

```