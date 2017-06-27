### 我的课程表

**请求地址**:
```
    GET     /course/my_courses/
```

**请求参数**:
```

```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
            "id": 2,
            "name": "北京校区一期项目",
            "course_num": 3,
            "current_course_num": 1,
            "my_courses": [
                {
                    "id": 2,
                    "project": 2,
                    "course_code": "6ZDGW28OL7",
                    "name": "小学语文",
                    "max_num": 50,
                    "credit": 3,
                    "professor": "陈冠希",
                    "start_time": "2017-06-29T08:00:00Z",
                    "end_time": "2017-06-29T12:00:00Z",
                    "create_time": "2017-06-19T16:07:11Z",
                    "address": "华府大道一段33号",
                    "syllabus": "/media/course/syllabus/RabbitMQ%E5%BB%B6%E6%97%B6%E6%B6%88%E6%81%AF%E5%AE%9E%E7%8E%B0%E6%96%B9%E6%A1%88_1.pdf"
                }
            ]
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```