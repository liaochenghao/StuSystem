### 检查是否可以创建订单

**请求地址**:
```
    GET     /order/check_order/
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
        "id": 33,
        "user": {
            "id": 2,
            "name": "Mary"
        },
        "project": {
            "id": 1,
            "campus": {
                "id": 3,
                "name": "南京校区",
                "campus_type": {
                    "id": 1,
                    "title": "北美暑校",
                    "create_time": "2017-07-04T00:00:00Z"
                },
                "info": "123",
                "create_time": "2017-06-14T23:41:05Z"
            },
            "name": "北京校区测试项目",
            "start_date": "2017-06-20",
            "end_date": "2017-07-01",
            "address": "长城路二段99号",
            "info": "这是项目须知，详情联系18608146540",
            "create_time": "2017-06-19T14:09:43Z",
            "apply_fee": 2000.0,
            "course_num": 3,
            "project_course_fee": [
                {
                    "id": 1,
                    "course_number": 1,
                    "course_fee": 1000.0,
                    "course_info": "1门"
                },
                {
                    "id": 2,
                    "course_number": 2,
                    "course_fee": 1800.0,
                    "course_info": "2门"
                },
                {
                    "id": 3,
                    "course_number": 3,
                    "course_fee": 2700.0,
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
        "create_time": "2017-07-06T15:51:37Z",
        "status": {
            "key": "TO_PAY",
            "verbose": "待支付"
        },
        "course_num": 3,
        "standard_fee": 4700.0,
        "pay_fee": null,
        "sales_man": {       # 销售人员
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
        }
    },
    "field_name": ""
}


无未完成订单时返回：

{
    "code": 100,        100code值有点特殊，为了和有未完成订单时code值做个区分
    "msg": "没有未完成的订单，可以创建",
    "data": {},
    "field_name": ""
}


```

**失败返回**：
```

```