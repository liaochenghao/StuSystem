### 某一学生学分转换详情

**请求地址**:
```
    GET     /admin/course_credit_switch/
```

**请求参数**:
```
{
    "user": int
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
            "id": 48,
            "post_datetime": null,      快递时间
            "post_channel": null,       快递方式
            "post_number": null,        快递单号
            "credit_switch_status": {
                "key": "PRE_POSTED",
                "verbose": "成绩待寄出"
            },
            "switch_img": null,         学分转换图片
            "user_info": {
                "id": 2,
                "name": "eee",
                "email": "826839564@qq.com",
                "wechat": "www"
            },
            "course": {
                "id": 16,
                "name": "Introduction to Biological Science 生物学概论",
                "course_code": "BIL 101"
            },
            "project": {
                "id": 11,
                "name": "暑期课程第一期"
            }
        }
    ],
    "field_name": ""
}

**失败返回**：
```

```