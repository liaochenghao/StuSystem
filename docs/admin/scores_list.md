###  学生成绩列表

**请求地址**:
```
    GET     /admin/user_info/[user_id]/scores/
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
            "score": 0,
            "score_grade": null,
            "user": 2,
            "order": 118,
            "course": {
                "id": 16,
                "course_code": "BIL 101",
                "name": "Introduction to Biological Science 生物学概论"
            },
            "project": {
                "id": 11,
                "name": "暑期课程第一期"
            }
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```