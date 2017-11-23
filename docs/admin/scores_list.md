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
            "score": 0,                             成绩
            "score_grade": "",                      课程等级
            "user": 6                               用户id
            "order": 77,                            订单id
            "course": 1                             课程id
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```