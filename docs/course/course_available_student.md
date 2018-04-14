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
    "data": [
        {
            "user_id": 594,
            "create_time": "2018-04-13T10:53:01.462865",
            "name": "吴梓恺",
            "sales_man": "Air",
            "wechat": "bryanwzk",
            "project": "杭州-五周项目"
        },
        {
            "user_id": 498,
            "create_time": "2018-04-14T00:10:02.289412",
            "name": "黄清龄",
            "sales_man": "Jack",
            "wechat": "Qingling1998",
            "project": "网课-第一期四周项目"
        },
        {
            "user_id": 586,
            "create_time": "2018-04-14T09:18:12.999681",
            "name": "王小萌",
            "sales_man": "Air",
            "wechat": "wangxiaomeng1997",
            "project": "网课-第二期四周项目"
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```