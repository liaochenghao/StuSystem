### 更新课程成绩

**请求地址**:
```
    PUT     /admin/user_course/confirm_course/
```

**请求参数**:
```
    {
        "user": int      用户id,
        "project": int   项目id
        "course": int    课程id
        "order": int     订单id
        "status": varchar  PASS--审核通过, NOPASS--审核不通过
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 16,
        "order": 78,
        "course": {
            "id": 5,
            "course_code": "3FGWTSYQXE",
            "name": "测试课程3",
            "credit": 3
        },
        "score": 88,
        "score_grade": "A",
        "reporting_time": "2017-07-25T16:01:03Z",
        "confirm_img": null,
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