### 学生选课

**请求地址**:
```
    POST      /source/user_course/
```

**请求参数**:
```
{
	"order": int 订单id 必填,
	"chart": int  必填,
	"course_ids": list 课程id列表
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "选课成功",
    "data": {},
    "field_name": ""
}

```

**失败返回**：
```

```