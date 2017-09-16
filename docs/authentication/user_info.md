### 获取用户信息

**请求地址**:
```
    GET     /auth/user/info/[user_id]/
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
            "id": 1,                            int     用户id
            "name": "yirantai",                 str     用户姓名,   最大长度30
            "email": "896275756@qq.com",        str     email，    最大长度30
            "wechat": "flyerweixin",            str     微信号      最大长度30
            "wcountry":  int,       意向国家
            "wcampus": ["北京校区", "上海校区"]   list     意向校区
            "cshool": "北京大学"                 str      当前学校    最大长度30
            "headimgurl": ""                    str      用户头像
            "sales_man":  {
                "id": 1,
                "name": "zhangsan",
                "email": "896254545@qq.com",
                "qr_code": "http://www.baidu.com",
                "wechat": "flyerweixin"
            }
        },
        "field_name": ""
    }
```

**失败返回**：
```

```