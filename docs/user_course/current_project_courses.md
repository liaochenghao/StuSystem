### 根据订单，项目，获取当前可选课程列表

**请求地址**:
```
    GET     /source/user_course/current_project_courses/
```

**请求参数**:
```
    {
        "order":    int   订单id， 必填
        "project":  int   项目id， 必填
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [                                                           # 当前项目所有可选课程信息
        {
            "id": 56,                                               # 课程id
            "course_code": "1",                                     # 课程代码
            "name": "Financial Accounting",                         # 课程名称
            "credit": 4,                                            # 课程学分
        },
    ]
    "field_name": ""
}
```

**失败返回**：
```

```