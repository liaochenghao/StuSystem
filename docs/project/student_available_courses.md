###  根据学生订单，项目获取允许选课列表

**请求地址**:
```
    GET     /source/project/[project_id]/student_available_courses/
```

**请求参数**:
```
    {
        "order":  int   订单id， 必填
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "chart": {
            "id": 1
        },
        "course_list": [
            {
                "id": 3,
                "course_code": "3",
                "name": "Introduction to Finance",
                "max_num": 20,
                "credit": 4,
                "create_time": "2018-01-15T12:22:05Z"
            },
            {
                "id": 4,
                "course_code": "4",
                "name": "Ethics in Banking",
                "max_num": 20,
                "credit": 4,
                "create_time": "2018-01-15T12:22:05Z"
            },
            ...
        ]
    }
    "field_name": ""
}
```

**失败返回**：
```

```