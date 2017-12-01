### 上传订单支付信息

**请求地址**:
```
    POST   /order/order_payment/
```

**请求参数**:
```
{
    "order":   int     订单id   必填
    "account_number":  varchar 支付账号  必填
    "account_name":   varchar  支付姓名  必填
    "opening_bank":   varchar  开户银行，选填
    "pay_date":        date  支付日期    必填
    "img":             Base64   确认图片,
    "amount": float   用户支付的金额
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 66,
        "user": {
            "id": 2,
            "name": "Mary"
        },
        "project": {
            "id": 2,
            "campus": {
                "id": 1,
                "name": "北京校区",
                "campus_type": {
                    "id": 1,
                    "title": "北美暑校",
                    "create_time": "2017-07-04T00:00:00Z"
                },
                "info": "123",
                "create_time": "2017-06-14T23:40:30Z"
            },
            "name": "北京校区一期项目",
            "start_date": "2017-06-20",
            "end_date": "2017-06-24",
            "address": "长城路二段99号",
            "info": "这是项目须知，详情联系18608146540",
            "create_time": "2017-06-20T15:39:48Z",
            "apply_fee": 1000,
            "course_num": 3,
            "project_course_fee": [
                {
                    "id": 4,
                    "course_number": 1,
                    "course_fee": 1200,
                    "course_info": "1门"
                },
                {
                    "id": 5,
                    "course_number": 2,
                    "course_fee": 2000,
                    "course_info": "2门"
                },
                {
                    "id": 6,
                    "course_number": 3,
                    "course_fee": 2700,
                    "course_info": "3门"
                }
            ]
        },
        "currency": {
            "key": "DOLLAR",
            "verbose": "美金"
        },
        "payment": {
            "key": "ALI_PAY",
            "verbose": "支付宝转账"
        },
        "create_time": "2017-07-08T16:24:37Z",
        "status": {
            "key": "TO_CONFIRM",
            "verbose": "待确认"
        },
        "course_num": 1,
        "standard_fee": 2200,
        "pay_fee": 1500,
        "sales_man": {
            "id": 14,
            "name": "anni"
        },
        "payment_info": {
            "id": 1,
            "account_number": "896275756@qq.com",
            "account_name": "邱雷",
            "opening_bank": null,
            "payment": {
                "key": "ALI_PAY",
                "verbose": "支付宝转账"
            }
        },
        "order_payed_info": {
            "id": 8,
            "order": 66,
            "account_number": "12345@qq.com",
            "account_name": "123123",
            "opening_bank": null,
            "pay_date": "2017-07-06"
        },
    },
    "field_name": ""
}
```

**失败返回**：
```

```