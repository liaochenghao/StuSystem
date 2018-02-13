### 最近一个订单

**请求地址**:
```
    GET     /order/last_order/
```

**请求参数**:
```
    无
```

**成功返回**：
```

有未完成订单时返回
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 4,
        "user": {
            "id": 2,
            "name": "潘思童"
        },
        "currency": {
            "key": "FOREIGN_CURRENCY",
            "verbose": "外币"
        },
        "payment": {
            "key": "ALI_PAY",
            "verbose": "支付宝转账"
        },
        "create_time": "2018-01-22T09:45:16Z",
        "modified_time": "2018-01-22T09:45:16Z",
        "status": {
            "key": "TO_CONFIRM",
            "verbose": "待确认"
        },
        "standard_fee": 30120,
        "pay_fee": 30120,
        "remark": null,
        "order_number": "2018012217443323",
        "charts": [
            {
                "id": 3,
                "project": {
                    "id": 1,
                    "campus": {
                        "id": 1,
                        "name": "北京校区",
                        "info": "上课地点：北京外国语大学",
                        "create_time": "2018-01-15T12:22:05Z",
                        "network_course": false
                    },
                    "name": "北京校区五周项目",
                    "start_date": "2018-06-04",
                    "end_date": "2018-07-06",
                    "address": "北京外国语大学",
                    "info": null,
                    "create_time": "2018-01-15T12:22:19Z",
                    "apply_fee": 2000,
                    "course_num": null,
                    "project_course_fee": [
                        {
                            "id": 482,
                            "course_number": 1,
                            "course_fee": 23120,
                            "course_info": "1门"
                        },
                        {
                            "id": 483,
                            "course_number": 2,
                            "course_fee": 23120,
                            "course_info": "2门"
                        },
                        {
                            "id": 484,
                            "course_number": 3,
                            "course_fee": 28120,
                            "course_info": "3门"
                        },
                        {
                            "id": 485,
                            "course_number": 4,
                            "course_fee": 33120,
                            "course_info": "4门"
                        }
                    ],
                    "applyed_number": 1,
                    "payed_number": 0
                },
                "course_num": 3,
                "course_fee": 30120,
                "create_time": "2018-01-22T03:48:19Z"
            }
        ],
        "payment_info": {
            "id": 3,
            "account_number": "scc@iauss.org",
            "account_name": "贝壳联投(武汉科技有限公司)",
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
        "order_payed_info": {
            "id": 4,
            "img": "http://42.51.8.152:8002/media/order/order_payment/微信图片_20170620150723.jpg",
            "order": 4,
            "remark": null
        },
        "sales_man": {
            "id": 18,
            "name": "Amy"
        },
        "course_to_select": false
    },
    "field_name": ""
}

无未完成订单时返回：

{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "course_to_select": false
    },
    "field_name": ""
}


```

**失败返回**：
```

```