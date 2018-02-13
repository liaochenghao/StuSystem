###  学分转换操作详情

**请求地址**:
```
    GET     /source/user_course/[id]/
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
    "data": {
        "id": 3,
        "course_id": 8,
        "credit_switch_status": {
            "key": "SWITCHED",
            "verbose": "学分已转换"
        },
        "order_id": 3,
        "status": {
            "key": "PASS",
            "verbose": "审课通过"
        },
        "post_datetime": "2018-02-02T11:12:52Z",
        "post_channel": "123456",
        "post_number": "dfda",
        "switch_img": "http://127.0.0.1:8001/media/project/result/photo/70277236478236737.jpg",
        "name": "Introduction to Modern Art",
        "chart": {
            "id": 2
        },
        "course_code": "8",
        "project": {
            "id": 5,
            "name": "武汉校区第一期四周项目"
        }
    },
    "field_name": ""
}
```

**失败返回**：
```

```