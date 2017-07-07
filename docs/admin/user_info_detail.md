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
    },
    "field_name": ""
}
```

**失败返回**：
```

```