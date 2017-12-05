### 当前项目已选课程

**请求地址**:
```
    GET  /admin/course/current_courses/
```

**请求参数**:
```
    {
        "user": int,
        "order": int,
        "project": int
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
            "id": 48,
            "project": 11,
            "order": 118,
            "course": {
                "id": 16,
                "course_code": "BIL 101",
                "name": "Introduction to Biological Science 生物学概论"
            }
        },
    ],
    "field_name": ""
}
```

**失败返回**：
```

```