###  学生成绩列表

**请求地址**:
```
    GET     /admin/user_info/[user_id]/scores/
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
            "project_name": "北京校区二期项目",       项目名称
            "course_code": "46QARX80KM",            课程代码
            "start_time": "2017-06-27T00:00:00Z",
            "end_time": "2017-07-19T00:00:00Z",
            "score": 0,                             成绩
            "score_grade": "",                      课程等级
            "user": 6
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```