### 获取当前已选课数量和, 课程总数及课程信息

**请求地址**:
```
    GET     /course/current_courses_info/
```

**请求参数**:
```
{
    "project": int      项目id
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
            "course_num": 1,            # 总课程数
            "current_course_num": 1,    # 已选课程数
            "project": {                # 项目信息
                "id": 10,
                "name": "冬季课程"
            },
            "order": {                  # 订单信息
                "id": 118
            },
            "chart_id": 2,              # chart_id
            "current_courses": [        # 已选课程信息
                {
                    "id": 15,
                    "course_code": "ART 12",
                    "name": "Western Art: Renaissance to the Present 西方艺术：文艺复兴时期至今"
                }
            ]
        },
    ],
    "field_name": ""
}
```

**失败返回**：
```

```