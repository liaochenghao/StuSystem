###  成绩单寄送地址列表

**请求地址**:
```
    PUT/PATCH     /admin/user_course_address/[user_id]/
```

**请求参数**:
```
{
    "province_post_code": ""        str     收件州/省的邮编         最大长度30
    "university": ""                str     大学名称                最大长度30
    "department": ""                str     院系名称                最大长度30  --选填
    "transfer_department": ""       str     转学分部门/办公楼       最大长度30
    "transfer_office": ""           str     具体办公室              最大长度30
    "address"：""                   str     收件详细地址            最大长度60  --选填
    "teacher_name"：""              str     收件老师姓名            最大长度30  --选填
    "phone":    ""                  str     联系电话                最大长度30
    "email": ""                     str     邮箱                    最大长度30  --选填

}
```

**成功返回**：
```

{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 42,
        "user_id": 2,
        "province_post_code": "342101111",
        "university": "加州大学",
        "department": "教务处",
        "transfer_department": "东八楼",
        "transfer_office": "2312A",
        "address": "加州大学教务处东八楼2312A室",
        "teacher_name": "lisa rong",
        "phone": "082-1231-2331",
        "email": "ldiw@ste.org"
    },
    "field_name": ""
}
```

**失败返回**：
```

```