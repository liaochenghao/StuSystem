###  学生信息列表

**请求地址**:
```
    GET     /auth/user/info/
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
            "user_id": 4,
            "name": "邱雷",
            "email": "896275756@qq.com",
            "cschool": "青蛙大学",                  学生当前所在学校
            "last_login": "2017-07-06T15:04:47Z",
            "personal_file": "已建档"              个人档案
        },
    ],
    "field_name": ""
}
```

**失败返回**：
```

```