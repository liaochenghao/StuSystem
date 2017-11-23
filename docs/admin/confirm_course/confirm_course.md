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
            "confirm_img": null,
            "status": {
                "key": "TO_UPLOAD",
                "verbose": "待上传"
            }
            "user": 6,
            "project": {
                "id": int,
                "name": str
            },
            "course": {
                "id":  int,
                "name": str,
                "course_code": str
            }
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```