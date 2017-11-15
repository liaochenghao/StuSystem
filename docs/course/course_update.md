### 创建校区

**请求地址**:
```
    PUT/PATCH   /source/course/[course_id]/
```

**请求参数**:
```
{
    "name":      str     课程名称     最大长度30
    "max_num":   int     最大选课人数
    "credit"     int     学分
    "max_num":  int        最大选课人数,
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 2,
        "project": 1,                       int     项目id
        "course_code": "6ZDGW28OL7",        str     课程代码
        "name": "小学语文",                  str     课程名称
        "max_num": 50,                      int     最大选课人数
        "credit": 3,                        int     学分
        "professor": "陈冠希",               str     教授
        "start_time": "2017-06-30T00:00:00Z",
        "end_time": "2017-06-30T04:00:00Z",
        "create_time": "2017-06-19T16:07:11Z",
        "address": "华府大道一段33号"          str     上课地点
        "syllabus": ""                       str    课程地址
        "current_course_num": 1              int    当前选课人数
    },
    "field_name": ""
}
```

**失败返回**：
```

```