### 更新用户档案信息

**请求地址**:
```
    PUT/PATCH       ／auth/user/info/[user_id]/personal_file/
```

**请求参数**:
```
    {
        "name":         str     中文名称
        "english_name": str     英文名称
        "email":        str     邮箱
        "gender":       str     MALE--男, FEMALE--女
        "id_number":    str     最大长度30
        "major":        str     专业
        "gpa"：         float   小数点后两位
        "birth_date":   date    出生日期
        "grade":        str     所在年级
        "phone":        str     phone

    }
```

**成功返回**：
```
    {
        "code": 0,
        "msg": "请求成功",
        "data": {
            "id": 2,
            "name": "阮国栋",
            "english_name": "Steve Curr",
            "email": "pst123@qq.com",
            "first_language": "Chinese",
            "ielts_scores": null,
            "wechat": "pst123",
            "gender": {
                "key": "MALE",
                "verbose": "男"
            },
            "id_number": "2",
            "birth_date": "1991-05-10",
            "grade": {
                "key": "GRADE_FOUR",
                "verbose": "大四"
            },
            "phone": "1860814654",
            "headimgurl": "http://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELozW1bvmf0U9tGnXmOs3DLrCCmRibCOnOGYkR8NwvexCN5gvFellRqet9U3IhqsUv9dtc4SXNQ55Q/132",
            "cschool": "武汉理工大学",
            "gpa": 3.3,
            "major": "软件工程"
        },
        "field_name": ""
    }

```
备注：gender为dict的key-verbose结构：
     示例： {"key": "MALE", "verbose": "男"} 或 {"key": "FEMALE", "verbose": "女"}
     grade为dict的key-verbose结构：
     示例： {"key": "grade_one", "verbose": "大一"}

**失败返回**：
```

```