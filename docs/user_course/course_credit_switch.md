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
                "id": 5,
                "name": "武汉校区第一期四周项目"
            },
            "order": {
                "id": 3
            },
            "chart": 2,
            "current_courses": [
                {
                    "id": 8,
                    "course_code": "8",
                    "name": "Introduction to Modern Art",
                    "professor": "somebody",
                    "start_time": "2018-01-30",
                    "end_time": "2018-02-28",
                    "address": "武汉理工大学",
                    "credit_switch_status": {
                        "key": null,
                        "verbose": null
                    },
                    "post_datetime": null,
                    "post_channel": null,
                    "post_number": null,
                    "switch_img": null
                },
                {
                    "id": 5,
                    "course_code": "5",
                    "name": "Western Art: Ancient to Medieval",
                    "professor": null,
                    "start_time": null,
                    "end_time": null,
                    "address": "武汉理工大学",
                    "credit_switch_status": {
                        "key": "SUCCESS",
                        "verbose": "学分转换成功"
                    },
                    "post_datetime": "2018-01-31T16:40:02Z",
                    "post_channel": "东风快递",
                    "post_number": "DF-41",
                    "switch_img": "http://42.51.8.152:8002/media/project/result/photo/70277236478236737.jpg"
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
    "credit_switch_status": str 必填  SUCCESS--学分转换成功，FAILURE--学分转换失败
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