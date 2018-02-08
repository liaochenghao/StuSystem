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
        "id": 2,
        "course_id": 5,
        "order_id": 3,
        "chart": {
            "id": 2
        },
        "project": {
            "id":  1,
            "name": "北京校区五周项目"
        }
        "credit_switch_status": {
            "key": "SWITCHED",
            "verbose": "学分已转换"
        },
        "post_datetime": "2018-01-31T16:40:02Z",
        "post_channel": "东风快递",
        "post_number": "DF-41",
        "switch_img": "http://127.0.0.1:8002/media/project/result/photo/70277236478236737.jpg",
        "name": "Western Art: Ancient to Medieval",
        "course_code": "5"
    },
    "field_name": ""
}
```

**失败返回**：
```

```