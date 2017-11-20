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
                "id": 11,
                "name": "暑期课程第一期"
            },
            "order": {
                "id": 118
            },
            "chart_id": 3,
            "current_courses": [
                {
                    "id": 15,
                    "course_code": "ART 12",
                    "name": "Western Art: Renaissance to the Present 西方艺术：文艺复兴时期至今",
                    "confirm_photo": "http://42.51.8.152/media/course/confirm_photo/test2.png",
                    "status": {
                        "key": "TO_CONFIRM",
                        "verbose": "待审核"
                    }
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

###  上传审课图片

**请求地址**:
```
    PUT     /course/[course_id]/upload_confirm_photo/
```

**请求参数**:
```
{
    "chart_id": int 必填  chart_id
    "order": int    必填  订单id
    "course": int   必填  课程id
    "confirm_photo": base64位字符串  必填 审课图片
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