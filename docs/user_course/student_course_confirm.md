###  获取审课信息

**请求地址**:
```
    GET     /source/user_course/student_confirm_course/
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
                    "status": {
                        "key": "TO_UPLOAD",
                        "verbose": "未审课"
                    },
                    "confirm_img": http://42.51.8.152:8002/media/course/confirm_img/70277236478236737_Nwcj2Yl.jpg
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

###  上传审课图片

**请求地址**:
```
    PUT     source/user_course/student_confirm_course/
```

**请求参数**:
```
{
    "chart": int        必填  商品id
    "order": int        必填  订单id
    "course": int       必填  课程id
    "confirm_img":          base64位字符串  必填 审课图片
    "confirm_remark":   选填  审课备注
}
```

**成功返回**：
```
{
  "code": 0,
  "msg": "操作成功",
  "data": {},
  "field_name": ""
}
```

**失败返回**：
```

```