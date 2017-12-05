### 当前订单，项目下可以选择的课程

**请求地址**:
```
    GET  /admin/course/available_courses/
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
            "id": 17,
            "course_code": "BIL 102",
            "name": "course 3",
            "credit": 3
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```