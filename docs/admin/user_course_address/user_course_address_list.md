###  成绩单寄送地址列表

**请求地址**:
```
    GET     /admin/user_course_address/[user_id]/
```

**请求参数**:
```

```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
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
        {
            "id": 43,
            "user_id": 3,
            "province_post_code": "34210111122",
            "university": "加州大学22",
            "department": "教务处22",
            "transfer_department": "东八楼22",
            "transfer_office": "2312A22",
            "address": "加州大学教务处东八楼2312A室22",
            "teacher_name": "lisa rong22",
            "phone": "082-1231-233122",
            "email": "ldiw@ste.org22"
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```