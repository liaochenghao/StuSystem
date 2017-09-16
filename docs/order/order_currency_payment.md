###   订单币种及支付方式

**请求地址**:
```
    GET     /order/order_currency_payment/
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
            "key": "DOLLAR",
            "verbose": "美金",
            "payment": [
                {
                    "key": "BANK",
                    "verbose": "银行转账"
                },
                {
                    "key": "PAY_PAL",
                    "verbose": "PAY_PAL支付"
                }
            ]
        },
        {
            "key": "RMB",
            "verbose": "人民币",
            "payment": [
                {
                    "key": "BANK",
                    "verbose": "银行转账"
                },
                {
                    "key": "ALI_PAY",
                    "verbose": "支付宝转账"
                },
                {
                    "key": "OFF_LINE",
                    "verbose": "面付"
                }
            ]
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```