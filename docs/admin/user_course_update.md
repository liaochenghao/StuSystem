### 更新课程成绩

**请求地址**:
```
    PATCH     /admin/user_course/[user_course_id]/
```

**请求参数**:
```
    {
        "score": int    课程成绩,
        "score_degree":  varchar    课程等级
        "reporting_time":   str     成绩录入时间
        "status": str    审课状态
    }
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
        "score": 88,
        "score_grade": "B",
        "reporting_time": "2017-07-23T00:00:00+08:00",
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