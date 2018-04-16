###     查询当前课程的所有学生

**请求地址**:
```
    GET     /source/course/[course_id]/course_available_student/
```

**请求参数**:
```
    project_id   int  选填 
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "student_list": [
            {
                "user_id": 586,
                "create_time": "2018-04-14T09:18:12.999681",
                "name": "王小萌",
                "sales_man": "Air",
                "wechat": "wangxiaomeng1997",
                "project": "网课-第二期四周项目"
            },
            {
                "user_id": 1690,
                "create_time": "2018-04-14T22:34:39.927381",
                "name": "薛拯",
                "sales_man": "Air",
                "wechat": "ayu__xz",
                "project": "网课-第二期四周项目"
            }
        ],
        "course_name": "Financial Accounting",
        "max_num": 20,
        "choose_num": 2
    },
    "field_name": ""
}
```

**失败返回**：
```

```