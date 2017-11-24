### 我的成绩

**请求地址**:
```
    GET     ／source/user_course/my_scores/
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
            "project": {
                "id": 11,
                "name": "暑期课程第一期"
            },
            "order": {
                "id": 118
            },
            "chart": 3,
            "current_courses": [
                {
                    "id": 15,
                    "course_code": "ART 12",
                    "name": "Western Art: Renaissance to the Present 西方艺术：文艺复兴时期至今",
                    "professor": "Steven Curry",
                    "start_time": "2017-11-16",
                    "end_time": "2017-11-16",
                    "address": "???????",
                    "score": 90,
                    "score_grade": "A",
                    "reporting_time": "2017-11-23T04:11:00Z"
                },
            ]
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```