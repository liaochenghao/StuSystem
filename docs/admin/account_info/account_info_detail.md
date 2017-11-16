### 账户详情

**请求地址**:
```
    GET     ／admin/account_info/[account_info_id]/
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