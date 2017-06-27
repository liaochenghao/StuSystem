### 我的项目

**请求地址**:
```
    GET    /course/project/my_project/
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
            "campus": {     校区信息
                "id": 1,
                "name": "北京校区",
                "campus_type": {    暑校类型
                    "id": 1,
                    "title": "北美暑校",
                    "create_time": "2017-06-14T23:38:14Z"
                },
                "info": "123",
                "create_time": "2017-06-14T23:40:30Z"
            },
            "name": "北京校区一期项目",     项目名称
            "start_date": "2017-06-20",
            "end_date": "2017-06-24",
            "address": "长城路二段99号",    项目地址
            "info": "这是项目须知，详情联系18608146540",  项目须知
            "create_time": "2017-06-20T15:39:48Z",
            "apply_fee": 1000,                      项目费用
            "course_num": 3,                        项目课程数量
            "current_course_num": 2,                当前已选课程数量
            "order_status": {                       订单支付状态
                "key": "PAYED",
                "verbose": "已支付"
            },
            "order_remark": null,                   该项目订单备注
            "my_courses": [                         已选择的课程
                 {
                    "id": 2,
                    "project": 1,                       int     项目id
                    "course_code": "6ZDGW28OL7",        str     课程代码
                    "name": "小学语文",                  str     课程名称
                    "max_num": 50,                      int     最大选课人数
                    "credit": 3,                        int     学分
                    "professor": "陈冠希",               str     教授
                    "start_time": "2017-06-30T00:00:00Z",
                    "end_time": "2017-06-30T04:00:00Z",
                    "create_time": "2017-06-19T16:07:11Z",
                    "address": "华府大道一段33号"          str     上课地点
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