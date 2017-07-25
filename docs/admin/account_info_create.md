### 账户创建

**请求地址**:
```
    POST     ／admin/account_info/
```

**请求参数**:
```
    {
        "account_number": str  必填  账户号
        "account_number": str  必填  账户名
        "opening_bank": str    选填  开户行(设置的是银行转账时，该字段必填，否则不传该字段)
        "payment": str         必填  付款方式(key值在/common/global_enums/接口中获取)

    }
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