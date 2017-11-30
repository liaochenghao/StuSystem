###  成绩单寄送地址列表

**请求地址**:
```
    GET     /admin/user_course_address/
```

**请求参数**:
```
{
    "user": int  必填
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
            "project": {        项目信息
                "id": 11,
                "name": "暑期课程第一期"
            },
            "course": {         课程信息
                "id": 16,
                "course_code": "BIL 101",
                "name": "Introduction to Biological Science 生物学概论"
            },
            "student_score_detail": {      寄送地址详情
                "id": 10,                  寄送地址id
                "department": "材料科学与工程学院",      收件人(部门)
                "phone": "18608146540",                收件电话
                "country": "美国",                      收件国家
                "post_code": "021878768687",            邮编
                "address": "纽约市布鲁克林区布鲁克林大道58号"      详细地址
            }
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```