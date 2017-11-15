### 创建项目与课程的关联

**请求地址**:
```
    POST     /source/course_project/
```

**请求参数**:
```
{
    "course": int 课程id  必填
    "project": int 项目id  必填
    "professor": str 教授名称 必填  max_length=30
    "start_time": datetime 开始时间 必填  格式：yyyy-MM-DD
    "end_time": datetime  开始时间  必填  格式：yyyy-MM-DD
    "address": str  上课地点  必填  max_length=100
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "关联成功",
    "data": {},
    "field_name": ""
}
```

**失败返回**：
```

```