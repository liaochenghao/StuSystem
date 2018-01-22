### 获取当前项目，选课数量,课程总数及课程详细信息

**请求地址**:
```
    GET     /source/user_course/current_project_courses/
```

**请求参数**:
```
    {
        "order":  int   订单id， 必填
    }
```

**成功返回**：
```
"code": 0,
    "msg": "请求成功",
    "data": {
        "course_num": 5,                                                # 当前订单可选课程总数
        "current_course": [                                             # 当前订单已选择课程课程
            {
                "course__course_code": "2"
            },
            {
                "course__course_code": "5"
            }
        ],
        "project_all_course": [                                         # 当前订单所有课程信息
            {
                "course_code": "1",                                     # 课程代码
                "name": "Financial Accounting",                         # 课程名称
                "max_num": 20,                                          # 最大容纳人数
                "credit": 4,                                            # 课程学分
                "courseproject__project__start_date": "2018-06-04",     # 项目开始时间
                "courseproject__project__end_date": "2018-07-06"        # 项目结束时间
            },
            {
                "course_code": "2",
                "name": "Managerial Accounting",
                "max_num": 20,
                "credit": 4,
                "courseproject__project__start_date": "2018-06-04",
                "courseproject__project__end_date": "2018-07-06"
            },

        ......

    ],
    "field_name": ""
}
```

**失败返回**：
```

```