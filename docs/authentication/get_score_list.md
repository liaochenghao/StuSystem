### 获取用户成绩寄送信息列表

**请求地址**:
```
    GET     /auth/user/score_detail/
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
    "data": [
        {
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
    ]
    "field_name": ""
}
```

**失败返回**：
```

```