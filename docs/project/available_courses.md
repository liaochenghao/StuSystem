###  新建课程关联时允许关联的课程列表

**请求地址**:
```
    GET     /source/project/[project_id]/available_courses/
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