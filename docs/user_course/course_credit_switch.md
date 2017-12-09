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
                "id": 11,
                "name": "暑期课程第一期"
            },
            "order": {
                "id": 118
            },
            "chart": 3,
            "current_courses": [
                {
                    "id": 15,
                    "course_code": "ART 12",
                    "name": "Western Art: Renaissance to the Present 西方艺术：文艺复兴时期至今",
                    "professor": "Steven Curry",
                    "start_time": "2017-11-16",
                    "end_time": "2017-11-16",
                    "address": "???????",
                    "switch_img": "http://42.51.8.152:8002/media/project/result/photo/test2_TdFjewg.png"
                    "credit_switch_status": {
                        "key": "PRE_POSTED",
                        "verbose": "成绩待寄出"
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