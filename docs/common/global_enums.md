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
    "account_currency": [
            {
                "key": "DOLLAR",
                "verbose": "美金"
            },
            {
                "key": "RMB",
                "verbose": "人民币"
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
    "user_grade": [             # 用户所在年级
            {
                "key": "GRADE_ONE",
                "verbose": "大一"
            },
            {
                "key": "GRADE_TWO",
                "verbose": "大二"
            },
            {
                "key": "GRADE_THREE",
                "verbose": "大三"
            },
            {
                "key": "GRADE_FOUR",
                "verbose": "大四"
            },
            {
                "key": "GRADE_FIVE",
                "verbose": "大五"
            }
        ],
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
    ],
    "user_role": [              # 用户角色
        {
            "key": "STUDENT",
            "verbose": "学生"
        },
        {
            "key": "ADMIN",
            "verbose": "管理员"
        },
        {
            "key": "MARKET",
            "verbose": "市场部"
        },
        {
            "key": "FINANCE",
            "verbose": "财务部"
        }
    ],
    "campus_country": [
        {
            "key": "NORTH_AMERICA",
            "verbose": "北美暑校"
        },
        {
            "key": "AUSTRALIA",
            "verbose": "澳洲暑校"
        }
    ]
},
"field_name": ""
}
```

**失败返回**：
```

```