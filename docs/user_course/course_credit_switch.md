### 学分转换结果

**请求地址**:
```
    GET     /source/user_course/course_credit_switch/
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
                "id": 4,
                "name": "成都校区五周项目",
                "start_time": "2018-07-02",
                "end_time": "2018-08-03"
            },
            "order": {
                "id": 1
            },
            "chart": 1,
            "current_courses": [
                {
                    "id": 17,
                    "course_id": 1,
                    "course_code": "1",
                    "name": "Financial Accounting",
                    "professor": "aass",
                    "start_time": "2018-02-07T17:43:34Z",
                    "end_time": "2018-02-07T19:43:38Z",
                    "address": "西南财经大学",
                    "credit_switch_status": {
                        "key": "PRE_POSTED",
                        "verbose": "成绩待寄出"
                    },
                    "post_datetime": "2018-02-02T11:12:52Z",
                    "post_channel": "123456",
                    "post_number": "dfda",
                    "switch_img": "http://42.51.8.152:8002/media/project/result/photo/70277236478236737.jpg"
                },
                {
                    "id": 1,
                    "course_id": 2,
                    "course_code": "2",
                    "name": "Managerial Accounting",
                    "professor": "asd",
                    "start_time": "2018-02-07T07:00:00Z",
                    "end_time": "2018-02-07T11:00:00Z",
                    "address": "西南财经大学",
                    "credit_switch_status": {
                        "key": "PRE_POSTED",
                        "verbose": "成绩待寄出"
                    },
                    "post_datetime": "2018-02-02T11:12:52Z",
                    "post_channel": "123456",
                    "post_number": "dfda",
                    "switch_img": "http://42.51.8.152:8002/media/project/result/photo/70277236478236737.jpg"
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

### 上传学分转换结果证明

**请求地址**:
```
    PUT     /source/user_course/course_credit_switch/
```

**请求参数**:
```
{
    "chart": int 必填  商品id
    "order": int    必填  订单id
    "course": int   必填  课程id
    "switch_img": base64位字符串  必填 审课图片,
    "switch_remark":   选填  转学分备注
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "图片上传成功"，
    "data": {}
}
```

**失败返回**：
```

```