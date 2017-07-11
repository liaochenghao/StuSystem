### 订单列表

**请求地址**:
```
      GET   /order/
```

**请求参数**:
```
   筛选条件
   {
        "currency":     str     支付币种
        "payment":      str     支付方式
        "status":       str     订单状态
   }
   currency, payment, status传入字段到/common/global_enums/接口中获取
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 76,
                "user": 1,
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
                    "key": "RMB",
                    "verbose": "人民币"
                },
                "payment": {
                    "key": "ALI_PAY",
                    "verbose": "支付宝转账"
                },
                "create_time": "2017-07-08T17:22:51Z",
                "status": {
                    "key": "CONFIRMED",
                    "verbose": "已确认"
                },
                "course_num": 3,
                "standard_fee": 3700,
                "pay_fee": 3000,
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
                    "id": 18,
                    "order": 76,
                    "account_number": "12345@qq.com",
                    "account_name": "123123",
                    "opening_bank": null,
                    "pay_date": "2017-07-06",
                    "img": null,
                    "amount": 999.99
                },
                "user_course": []
            },
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```