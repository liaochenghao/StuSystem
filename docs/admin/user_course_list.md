### 所有学生成绩列表

**请求地址**:
```
    GET     /admin/user_course/
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
        "count": 4,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 14,
                "order": 77,
                "course": {
                    "id": 2,
                    "course_code": "6ZDGW28OL7",    课程代码
                    "name": "大学通识课一",   课程名称
                    "credit": 3             学分
                },
                "score": 0,                 成绩
                "score_grade": null,        成绩等级
                "reporting_time": null,     录入时间
                "confirm_photo": null,
                "status": {
                    "key": "TO_UPLOAD",
                    "verbose": "待上传"
                },
                "user_info": {              用户信息
                    "id": 1,
                    "name": "zxc",
                    "email": "xcz1899@163.com",
                    "wechat": "34343"
                }
            },
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```