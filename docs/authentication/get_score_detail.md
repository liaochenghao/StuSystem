### 获取用户成绩寄送地址详情

**请求地址**:
```
    GET     /auth/user/score_detail/[score_detail_id]/
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
            "id": 42,
            "user": 2,
            "province_post_code": "342101",
            "university": "加州大学",
            "department": "教务处",
            "transfer_department": "东八楼",
            "transfer_office": "2312A",
            "address": "加州大学教务处东八楼2312A室",
            "teacher_name": "lisa rong",
            "phone": "082-1231-2331",
            "email": "ldiw@ste.org"
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```