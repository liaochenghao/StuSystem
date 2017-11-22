###   更新学分转换

**请求地址**:
```
    PUT/PATCH     /admin/course_credit_switch/[id]/
```

**请求参数**:
```
    {
        "post_datetime":    str     快递时间
        "post_channel": str     快递方式
        "post_number":  str     快递单号
        "credit_switch_status":       str     状态值(响应状态值在/common/global_enums/接口中获取)
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 4,
        "project": {
            "id": 2,
            "campus_name": "北京校区",
            "name": "北京校区一期项目"
        },
        "post_datetime": "2017-07-25",
        "post_channel": "DHL",
        "post_number": "56468987243131",
        "credit_switch_status": {
            "key": "POSTED",
            "verbose": "成绩单已寄出"
        },
        "img": null,
        "user_info": {
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