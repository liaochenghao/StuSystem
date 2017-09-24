###   微信中分配销售顾问

**请求地址**:
```
    GET     /auth/user/assign_sales_man/
```

**请求参数**:
```
    {
        "code": ""      微信网页认证的code值
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 1,
        "name": "zhangsan",
        "email": "896254545@qq.com",
        "qr_code": "http://www.baidu.com",
        "wechat": "flyerweixin"
    },
    "field_name": ""
}
```

**失败返回**：
```

```