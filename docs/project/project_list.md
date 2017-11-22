### 获取项目列表

**请求地址**:
```
    GET   /source/project/
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
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 10,
                "campus": {
                    "id": 18,
                    "name": "武汉校区",
                    "info": "针对国际业务",
                    "create_time": "2017-11-14T09:14:48Z"
                },
                "name": "冬季课程",
                "start_date": "2017-12-25",
                "end_date": "2018-01-12",
                "address": "武汉市",
                "info": "2017年12月25日至2018年1月12日（3周课程）",
                "create_time": "2017-11-14T10:06:32Z",
                "apply_fee": 2000,
                "course_num": 4,
                "applyed_num": 0,    申请人数
                "payed_num": 0,  支付人数
                "project_course_fee": [
                    {
                        "id": 61,
                        "course_number": 1,
                        "course_fee": 23120,
                        "course_info": "1门"
                    }
                ]
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```