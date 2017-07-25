### 账户列表

**请求地址**:
```
    GET     ／admin/account_info/
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
        "account_number": "6217234402000423137",        账户号
        "account_name": "李总",                          账户名
        "opening_bank": "工商银行",                      开户行(可能为空字符串)
        "payment": {                                    支付方式
            "key": "BANK",
            "verbose": "银行转账"
        }
    },
    "field_name": ""
}
```

**失败返回**：
```

```