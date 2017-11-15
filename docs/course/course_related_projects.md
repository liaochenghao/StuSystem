###  课程关联项目

**请求地址**:
```
    GET     /source/course/[course_id]/related_projects/
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
    "data": {
        "id": 15,
        "course_code": "ART 12",
        "name": "Western Art: Renaissance to the Present 西方艺术：文艺复兴时期至今",
        "max_num": 100,
        "credit": 4,
        "create_time": "2017-11-14T10:37:48Z",
        "related_projects": [
            {
                "id": 1,
                "course": 15,
                "project": {     关联项目
                    "id": 10,
                    "campus": {
                        "id": 18,
                        "name": "武汉校区",
                        "info": "针对国际业务",
                        "create_time": "2017-11-14T09:14:48Z",
                        "network_course": false
                    },
                    "name": "冬季课程",
                    "start_date": "2017-12-25",
                    "end_date": "2018-01-12",
                    "address": "武汉市",
                    "info": "2017年12月25日至2018年1月12日（3周课程）",
                    "create_time": "2017-11-14T10:06:32Z",
                    "apply_fee": 2000,
                    "course_num": 4,
                    "project_course_fee": [
                        {
                            "id": 65,
                            "course_number": 1,
                            "course_fee": 23120,
                            "course_info": "1门"
                        },
                        {
                            "id": 66,
                            "course_number": 2,
                            "course_fee": 23120,
                            "course_info": "2门"
                        },
                        {
                            "id": 67,
                            "course_number": 3,
                            "course_fee": 28120,
                            "course_info": "3门"
                        }
                    ]
                },
                "create_time": "2017-11-15T03:04:52Z",
                "professor": "Iron Musk",
                "start_time": "2017-11-15",
                "end_time": "2017-11-29",
                "address": "武汉大学地质楼"
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```