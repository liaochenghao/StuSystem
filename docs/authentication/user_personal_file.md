### 获取用户档案信息

**请求地址**:
```
    GET     /auth/user/info/[user_id]/personal_file/
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
     示例： {"key": "grade_one", "verbose": "大一"} 等
```

**失败返回**：
```

```