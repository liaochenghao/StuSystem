### 获取全局的enums

**请求地址**:
```
    GET     /common/global_enums/
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
    "user_info_gender": [                   # 用户性别信息
        {
            "key": "MALE",
            "verbose": "男"
        },
        {
            "key": "FEMALE",
            "verbose": "女"
        },
        "order_payment": [                  # 订单支付方式
            {
                "key": "ON_LINE",
                "verbose": "线上支付"
            },
            {
                "key": "TRANSFER_ACCOUNT",
                "verbose": "转账"
            },
            {
                "key": "OFF_LINE",
                "verbose": "面付"
            }
        ],
        "order_currency": [                 # 订单支付币种
            {
                "key": "DOLLAR",
                "verbose": "美金"
            },
            {
                "key": "RMB",
                "verbose": "人民币"
            }
        ],
        "order_status": [                   # 订单状态
            {
                "key": "TO_PAY",
                "verbose": "待支付"
            },
            {
                "key": "PAYED",
                "verbose": "已支付"
            }
        ],
         "user_status": [                   # 用户的状态
            {
                "key": "NEW",
                "verbose": "新关注"
            },
            {
                "key": "CONTACTED",
                "verbose": "已联系"
            }
    },
"field_name": ""
}
```

**失败返回**：
```

```