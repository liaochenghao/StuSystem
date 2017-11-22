###     用户成绩邮寄信息创建

**请求地址**:
```
   POST     ／auth/user/score_detail/
```

**请求参数**:
```
{
    "department": ""        str     收件人部门   最大长度30
    "phone":    ""          str     收件联系电话 最大长度30
    "country": ""           str     收件国家    最大长度30
    "post_code": ""         str     邮编       最大长度30
    "address"：""           str      收件详细地址  最大长度60
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 1,
        "user": 1,                          int     用户id
        "department": "英语部",              str     收件人/部门
        "phone": "010-2014567",             str     收件联系电话
        "country": "中国",                   str     收件国家
        "post_code": "631741",              str      邮编
        "address": "北京大学昌平区E栋1233号"   str     详细地址
    },
    "field_name": ""
}
```

**失败返回**：
```

```