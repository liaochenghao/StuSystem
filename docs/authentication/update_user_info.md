### 更新用户信息

**请求地址**:
```
    PUT/PATCH   /auth/user/info/[user_id]/
```

**请求参数**:
```
    {
        "name":         str   姓名,   最大长度30
        "email":        str   email   最大长度30
        "wechat"：       str  微信号    最大长度30
        "wcountry"：      list    意向学校
        "wcampus"：      list    意向校区
        "cshool"：       str     当前学校    最大长度30
    }
```

```
备注： 传入wcountry参数时，list中元素为str，如["美国"， "加拿大"]
      传入wcountry参数时，list中元素为int校区的id值， 如[1,2,3]
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 1,
        "name": "yirantai",
        "email": "896275756@qq.com",
        "wechat": "flyerweixin",
        "wcountry": [
            "加拿大",
            "美国"
        ],
        "wcampus": [
            "北京校区",
            "上海校区"
            ],
        "cschool": "北京大学"
    },
"field_name": ""
}
```

**失败返回**：
```

```