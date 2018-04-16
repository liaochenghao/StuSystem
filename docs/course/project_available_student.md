###     查询当前课程的所有学生

**请求地址**:
```
    GET     /source/project/[project_id]/project_available_student/
```

**请求参数**:
```
    page   分页
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "count": 4,
        "data": [
            {
                "user_id": 1536,
                "name": "殷子涵",
                "wechat": "Rose-Dnsn",
                "email": "513606535@qq.com",
                "sales_man": "暑校小助手",
                "student_status": "TO_CHOOSE_COURSE",
                "university": null
            },
            {
                "user_id": 677,
                "name": "王浩秋",
                "wechat": "WuWaA_WeChat",
                "email": "wu.wa.a@qq.com",
                "sales_man": "Air",
                "student_status": "PICKUP_COURSE",
                "university": null
            },
            {
                "user_id": 625,
                "name": "石亦佳",
                "wechat": "973681129",
                "email": "973681129@qq.com",
                "sales_man": "Air",
                "student_status": "PICKUP_COURSE",
                "university": null
            },
            {
                "user_id": 533,
                "name": "赖祺玮",
                "wechat": "1370791949",
                "email": "1370791949@qq.com",
                "sales_man": "Sue",
                "student_status": "TO_CHOOSE_COURSE",
                "university": null
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```