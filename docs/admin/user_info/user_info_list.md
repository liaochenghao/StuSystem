###  学生信息列表

**请求地址**:
```
    GET     /admin/user_info/
```

**请求参数**:
```
   筛选条件(支持模糊搜索)
   {
        "name":     str 用户姓名
        "email":    str 邮件
        "wechat":   str 微信号
   }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "count": 1,
        "next": null,               上一页地址
        "previous": null,           下一页地址
        "results": [
            {
                "user_id": 4,
                "name": "邱雷",
                "email": "896275756@qq.com",
                "cschool": "青蛙大学",
                "last_login": "2017-07-06T15:04:47Z",
                "wechat":   "",
                "status": {
                    "key": "NEW",
                    "verbose": "新建用户"
                }
                "channel": {
                    'id': 9  int,
                    'name': '测试渠道',
                    'create_time': "2017-09-17T06:25:23Z"
                }
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```