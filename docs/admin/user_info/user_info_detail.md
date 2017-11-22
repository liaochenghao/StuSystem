###   学生信息详情

**请求地址**:
```
    GET     /admin/user_info/[user_id]/
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
        "user_id": 6,
        "name": "杨骐彰",
        "email": "yqz0203@hotmail.com",
        "first_name": "Yang",
        "last_name": "Qizhang",
        "gender": {
            "key": "MALE",
            "verbose": "男"
        },
        "id_number": "511321199202035835",
        "wechat": "yigelaile5",
        "cschool": "四川大学",
        "major": "计算机科学",
        "graduate_year": "2017-07",
        "gpa": 1
        "user_info_remark": [
            {
                "id": 4,
                "remark": "I Love you not because who you are!",
                "create_time": "2017-07-07T15:31:23Z"
            },
        ],
        "user_coupon": [
            {
                "user": 20,
                "id": 1,
                "info": "??I????",
                "start_time": "2017-06-18T16:40:49Z",
                "end_time": "2017-06-29T16:40:53Z",
                "coupon_code": "HGENY0X92N"
            }
        ],
        "channel": {
                    'id': 9  int,
                    'name': '测试渠道',
                    'create_time': "2017-09-17T06:25:23Z"
                }
    },
    "field_name": ""
}
```

**失败返回**：
```

```