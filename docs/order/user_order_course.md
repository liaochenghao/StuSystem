### 获取当前用户所有订单，选课信息，审课

**请求地址**:
```
    GET     /order/user_order_course/
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
            "id": 77,
            "user": {
                "id": 2,
                "name": "Mary"
            },
            "project": {
                "id": 2,
                "campus": {
                    "id": 1,
                    "name": "北京校区",
                    "campus_type": {
                        "id": 1,
                        "title": "北美暑校",
                        "create_time": "2017-07-04T00:00:00Z"
                    },
                    "info": "123",
                    "create_time": "2017-06-14T23:40:30Z"
                },
                "name": "北京校区一期项目",
                "start_date": "2017-06-20",
                "end_date": "2017-06-24",
                "address": "长城路二段99号",
                "info": "这是项目须知，详情联系18608146540",
                "create_time": "2017-06-20T15:39:48Z",
                "apply_fee": 1000,
                "course_num": 3,
                "project_course_fee": [
                    {
                        "id": 4,
                        "course_number": 1,
                        "course_fee": 1200,
                        "course_info": "1门"
                    },
                    {
                        "id": 5,
                        "course_number": 2,
                        "course_fee": 2000,
                        "course_info": "2门"
                    },
                    {
                        "id": 6,
                        "course_number": 3,
                        "course_fee": 2700,
                        "course_info": "3门"
                    }
                ]
            },
            "currency": "RMB",
            "payment": "ALI_PAY",
            "create_time": "2017-07-08T17:40:45Z",
            "status": "CONFIRMED",
            "course_num": 3,
            "standard_fee": 3700,
            "pay_fee": 3500,
            "sales_man": {      销售人员
                "id": 14,
                "name": "anni"
            },
            "remark": null,
            "user_course": [
                {
                    "id": 2,
                    "course_code": "6ZDGW28OL7",
                    "name": "大学通识课一",
                    "max_num": 50,
                    "credit": 3,
                    "professor": "Kobe",
                    "start_time": "2017-06-29T08:00:00Z",
                    "end_time": "2017-06-29T12:00:00Z",
                    "create_time": "2017-06-19T16:07:11Z",
                    "address": "华府大道一段33号",
                    "syllabus": "/media/course/syllabus/%E7%B2%BE%E8%8B%B1%E8%AE%B8%E5%8F%AF.jpeg",
                    "confirm_course": {
                        "score": 0,
                        "score_grade": null,
                        "reporting_time": null,
                        "confirm_img": null,
                        "status": {
                            "key": "TO_UPLOAD",
                            "verbose": "待上传"
                        }
                    }
                },
                {
                    "id": 3,
                    "course_code": "8BDJROMSCW",
                    "name": "大学通识课二",
                    "max_num": 50,
                    "credit": 3,
                    "professor": "Lebron",
                    "start_time": "2017-06-30T00:00:00Z",
                    "end_time": "2017-06-30T04:00:00Z",
                    "create_time": "2017-06-19T16:11:37Z",
                    "address": "大法进水看到回复看见啊",
                    "syllabus": "/media/course/syllabus/%E8%90%A5%E4%B8%9A%E6%89%A7%E7%85%A7.jpeg",
                    "confirm_course": {
                        "score": 0,
                        "score_grade": null,
                        "reporting_time": null,
                        "confirm_img": null,
                        "status": {
                            "key": "TO_UPLOAD",
                            "verbose": "待上传"
                        }
                    }
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