### 获取课程列表

**请求地址**:
```
    GET   /source/course/
```

**请求参数**:
```
筛选条件
{
    "project":      int     根据project进行筛选
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 2,
                "course_code": "6ZDGW28OL7",        str     课程代码
                "name": "小学语文",                  str     课程名称
                "max_num": 50,                      int     最大选课人数
                "credit": 3,                        int     学分
                "create_time": "2017-06-19T16:07:11Z",
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```