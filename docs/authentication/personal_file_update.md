### 更新用户档案信息

**请求地址**:
```
    PUT/PATCH       ／auth/user/info/[user_id]/personal_file/
```

**请求参数**:
```
    {
        "first_name":   str     最大长度30
        "last_name":    str     最大长度30
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
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 1,
        "name": "yirantai",                     str   用户姓名
        "email": "896275756@qq.com",            str   email
        "wechat": "flyerweixin",                str   微信号
        "cschool": "北京大学",                   str   所在学校
        "first_name": null,                     str
        "last_name": null,                      str
        "gender": null,                         dict   性别
        "id_number": null,                      str    身份证号／护照号
        "major": null,                          str    专业
        "graduate_year": null,                  str    预计毕业年份
        "gpa": null                             int    GPA值
        "birth_date":                           date    出生日期
        "grade":                                dict     所在年级
        "phone":                                str     phone
    },
    "field_name": ""
}
```

```
备注：gender为dict的key-verbose结构：
     示例： {"key": "MALE", "verbose": "男"} 或 {"key": "FEMALE", "verbose": "女"}
     grade为dict的key-verbose结构：
     示例： {"key": "grade_one", "verbose": "大一"}

**失败返回**：
```

```