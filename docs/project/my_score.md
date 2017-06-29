### 根据项目获取课程信息,成绩信息

**请求地址**:
```
    GET     /course/project/my_scores/
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
            "id": 2,
            "name": "北京校区一期项目",         项目名称
            "create_time": "2017-06-20T15:39:48Z",      项目创建时间
            "course": [
                {
                    "id": 2,
                    "course_code": "6ZDGW28OL7",        课程代码
                    "name": "小学语文",                  课程名称
                    "create_time": "2017-06-19T16:07:11Z",
                    "course_score": {                   课程成绩信息
                        "score": 0,                     分数
                        "score_grade": null,            等级
                        "reporting_time": null          录入时间
                    }
                },
            ]
        },
    ],
    "field_name": ""
}
```

**失败返回**：
```

```