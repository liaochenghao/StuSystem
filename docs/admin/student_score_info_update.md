###  成绩单寄送地址

**请求地址**:
```
    PATCH／PUT    /admin/student/score_info/[id]/
```

**请求参数**:
```
{
    "department": ""
    "phone": ""
    "country": ""
    "post_code": ""
    "address": ""
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "user": 4,
        "department": "英语部",                    邮寄部门
        "phone": "010-2014567",                   联系电话
        "country": "中国",                         国家
        "post_code": "631741",                    邮编
        "address": "北京大学昌平区E栋1233号"         详细地址
    },
    "field_name": ""
}
```

**失败返回**：
```

```