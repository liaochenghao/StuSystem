### 账户更新

**请求地址**:
```
    PUT/PATCH     ／admin/account_info/[account_info_id]/
```

**请求参数**:
```
    {
        "account_number": str  必填  账户号
        "account_number": str  必填  账户名
        "opening_bank": str    选填  开户行(设置的是银行转账时，该字段必填，否则不传该字段)
        "payment": str         必填  付款方式(key值在/common/global_enums/接口中获取)
        "currency":  str       必填  默认RMB
        "swift_code":  str     选填  当currency为DOLLAR时必填
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 3,
        "account_number": "896275756@qq.com",
        "account_name": "邱雷",
        "opening_bank": null,
        "payment": {
            "key": "ALI_PAY",
            "verbose": "支付宝转账"
        },
        "currency": {
            "key": "RMB",
            "verbose": "人民币"
        },
        "swift_code": null
    },
    "field_name": ""
}
```

**失败返回**：
```

```