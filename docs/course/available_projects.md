###     新建项目关联时允许操作的项目列表

**请求地址**:
```
    GET     /source/course/[course_id]/available_projects/
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
            "id": 12,
            "campus": {
                "id": 18,
                "name": "武汉校区",
                "info": "针对国际业务",
                "create_time": "2017-11-14T09:14:48Z",
                "network_course": false
            },
            "name": "暑期课程第二期",
            "start_date": "2018-06-04",
            "end_date": "2018-06-29",
            "address": "武汉市",
            "info": "2017年12月25日至2018年1月12日（3周课程）",
            "create_time": "2017-11-15T01:21:06Z",
            "apply_fee": 2000,
            "course_num": 4,
            "project_course_fee": [
                {
                    "id": 72,
                    "course_number": 1,
                    "course_fee": 23120,
                    "course_info": "1门"
                },
                {
                    "id": 73,
                    "course_number": 2,
                    "course_fee": 23120,
                    "course_info": "2门"
                },
                {
                    "id": 74,
                    "course_number": 3,
                    "course_fee": 28120,
                    "course_info": "3门"
                },
                {
                    "id": 75,
                    "course_number": 4,
                    "course_fee": 33120,
                    "course_info": "4门"
                }
            ],
            "applyed_number": 0,
            "payed_number": 0
        },
    ],
    "field_name": ""
}
```

**失败返回**：
```

```