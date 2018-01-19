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
                "id": 1,
                "user": 1,                              int     用户id
                "province_post_code": "123456"          str     收件州/省的邮编
                "university": "北京大学"                str     大学名称
                "department": "英语部",                 str     院系名称
                "transfer_department": ""               str     转学分部门/办公楼
                "transfer_office": ""                   str     具体办公室
                "address": "北京大学昌平区E栋1233号"    str     详细地址
                "teacher_name"："abc"                   str     收件老师姓名
                "phone": "010-2014567",                 str     收件联系电话
                "email": ""                             str     邮箱
            }
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```