###  学生审课记录列表

**请求地址**:
```
    GET     /admin/user_info/[user_id]/confirm_course/
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
            "project_name": "北京校区二期项目",
            "course_code": "46QARX80KM",
            "syllabus": "",
            "confirm_photo": null,
            "status": {
                "key": "TO_UPLOAD",
                "verbose": "待上传"
            }
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```