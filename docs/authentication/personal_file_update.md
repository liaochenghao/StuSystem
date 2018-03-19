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
        "first_language":str     所在年级
        "ielts_scores": str     所在年级
        "cshool":       str     学校
        "phone":        str     phone
        "valid_sales_man":  bool  判断是否添加顾问
    }
```

**成功返回**：
```
 {
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 110,
        "name": "13444",
        "english_name": null,
        "email": "40987879@qq.com",
        "first_language": null,
        "ielts_scores": null,
        "wechat": "48484848",
        "gender": {
            "key": "MALE",
            "verbose": "男"
        },
        "id_number": null,
        "birth_date": null,
        "grade": {
            "key": "GRADE_ONE",
            "verbose": "大一"
        },
        "phone": null,
        "headimgurl": "http://thirdwx.qlogo.cn/mmopen/vi_32/nVMLr1AgPVPqCvgGl1CbPuqLfODkjZibTiaxQBwHp0StPt9lvTiaStxA3m1QRF9iap1j38f4qX61BiaRCf6q3a6EbDQ/132",
        "cschool": "武汉理工大学",
        "major": "软件工程",
        "gpa": 0,
        "valid_sales_man": false
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