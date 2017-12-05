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
    "data": [
        {
            "id": 23,
            "course_code": "BIL 108",
            "name": "course 9",
            "max_num": 100,
            "credit": 3,
            "create_time": "2017-11-29T18:03:26Z"
        },
    ],
    "field_name": ""
}
```

**失败返回**：
```

```