### 创建课程

**请求地址**:
```
    POST   /source/course/
```

**请求参数**:
```
{
    "name":      str     课程名称     最大长度30
    "credit"     int     学分
    "max_num":  int        最大选课人数,
    "course_code":  str  必填  课程代码 最大长度30
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 2,
        "course_code": "6ZDGW28OL7",        str     课程代码
        "name": "小学语文",                  str     课程名称
        "max_num": 50,                      int     最大选课人数
        "credit": 3,                        int     学分
        "create_time": "2017-06-19T16:07:11Z",
    },
    "field_name": ""
}
```

**失败返回**：
```

```