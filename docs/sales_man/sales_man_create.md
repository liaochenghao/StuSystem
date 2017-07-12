###  创建销售顾问

**请求地址**:
```
    POST    /admin/sales_man/
```

**请求参数**:
```
    {
        "name":  str    姓名      必填  最大长度30
        "wechat": str   微信号    必填  最大长度30
        "email":  str   邮箱      必填  最大长度30
        "qr_code": Base64   二维码  必填
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
        "wechat": "xiubweixin",
        "email": "896254545@qq.com",
        "qr_code": "http://127.0.0.1:8002/media/http%3A/www.baidu.com"
    },
    "field_name": ""
}
```

**失败返回**：
```

```