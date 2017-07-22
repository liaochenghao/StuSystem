### 某一课程成绩详情

**请求地址**:
```
    GET     /admin/user_course/[user_course_id]/
```

**请求参数**:
```

```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 14,
        "order": 77,
        "course": {
            "id": 2,
            "course_code": "6ZDGW28OL7",
            "name": "大学通识课一",
            "credit": 3
        },
        "score": 0,
        "score_grade": null,
        "reporting_time": null,
        "confirm_photo": null,
        "status": {
            "key": "TO_UPLOAD",
            "verbose": "待上传"
        },
        "user_info": {
            "id": 1,
            "name": "zxc",
            "email": "xcz1899@163.com",
            "wechat": "34343"
        }
    },
    "field_name": ""
}
```

**失败返回**：
```

```