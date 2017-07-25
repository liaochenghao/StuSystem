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
    "account_payment": [
            {
                "key": "ALI_PAY",
                "verbose": "支付宝转账"
            },
            {
                "key": "BANK",
                "verbose": "银行转账"
            }
        ],
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
            },
         "project_result": [            # 成绩单寄送状态
            {
                "key": "POSTED",
                "verbose": "成绩单已寄出"
            },
            {
                "key": "RECEIVED",
                "verbose": "学校已收到"
            },
            {
                "key": "SUCCESS",
                "verbose": "学分转换成功"
            },
             {
                "key": "FAILURE",
                "verbose": "学分转换失败"
            }
        ],
        "user_course_status": [         # 学生审课状态
            {
                "key": "TO_UPLOAD",
                "verbose": "待上传"
            },
            {
                "key": "TO_CONFIRM",
                "verbose": "待审核"
            },
            {
                "key": "PASS",
                "verbose": "通过"
            }
        ],
        "coupon_status": [          # 优惠券使用情况
            {
                "key": "TO_USE",
                "verbose": "待使用"
            },
            {
                "key": "LOCKED",
                "verbose": "被锁定"
            },
            {
                "key": "USED",
                "verbose": "已使用"
            }
        ]
    },
"field_name": ""
}
```

**失败返回**：
```

```