###  成绩单寄送地址

**请求地址**:
```
    GET    /admin/student/score_info/
```

**请求参数**:
```
{
    "user": int  必填
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
            "id":  10                                寄送地址id
            "user": 4,
            "department": "英语部",                    邮寄部门
            "phone": "010-2014567",                   联系电话
            "country": "中国",                         国家
            "post_code": "631741",                    邮编
            "address": "北京大学昌平区E栋1233号"         详细地址
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```