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
            "user": 1,                          int     用户id
            "department": "英语部",              str     收件人/部门
            "phone": "010-2014567",             str     收件联系电话
            "country": "中国",                   str     收件国家
            "post_code": "631741",              str      邮编
            "address": "北京大学昌平区E栋1233号"   str     详细地址
        }
    ]
    "field_name": ""
}
```

**失败返回**：
```

```