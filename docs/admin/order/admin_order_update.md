### 管理员订单详情

**请求地址**:
```
      PUT/PATCH   /admin/order/[order_id]/
```

**请求参数**:
```
{
    "status": "CONFIRMED"   -- 确认订单
    "status": "CONFIRM_FAILED"  -- 支付认证失败
    ""
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 118,
        "user": {
            "id": 2,
            "name": "Mary"
        },
        "currency": {
            "key": "RMB",
            "verbose": "人民币"
        },
        "payment": {
            "key": "BANK",
            "verbose": "银行转账"
        },
        "create_time": "2017-11-15T10:03:38Z",
        "modified_time": "2017-11-15T10:31:07Z",
        "status": {
            "key": "TO_CONFIRM",
            "verbose": "待确认"
        },
        "standard_fee": 50240,
        "pay_fee": 50240,
        "remark": null,
        "sales_man": {
            "id": 14,
            "name": "anni"
        },
        "charts": [
            {
                "id": 2,
                "project": {
                    "id": 10,
                    "campus": {
                        "id": 18,
                        "name": "武汉校区",
                        "info": "针对国际业务",
                        "create_time": "2017-11-14T09:14:48Z",
                        "network_course": false
                    },
                    "name": "冬季课程",
                    "start_date": "2017-12-25",
                    "end_date": "2018-01-12",
                    "address": "武汉市",
                    "info": "2017年12月25日至2018年1月12日（3周课程）",
                    "create_time": "2017-11-14T10:06:32Z",
                    "apply_fee": 2000,
                    "course_num": 4,
                    "project_course_fee": [
                        {
                            "id": 65,
                            "course_number": 1,
                            "course_fee": 23120,
                            "course_info": "1门"
                        },
                        {
                            "id": 66,
                            "course_number": 2,
                            "course_fee": 23120,
                            "course_info": "2门"
                        },
                        {
                            "id": 67,
                            "course_number": 3,
                            "course_fee": 28120,
                            "course_info": "3门"
                        }
                    ]
                },
                "course_num": 1,
                "course_fee": 23120,
                "create_time": "2017-11-15T07:06:14Z",
                "stu_score_detail": {
                    "id": 10,
                    "user": 2,
                    "department": "材料科学与工程学院",
                    "phone": "18608146540",
                    "country": "美国",
                    "post_code": "021878768687",
                    "address": "纽约市布鲁克林区布鲁克林大道58号"
                }
            },
        ],
        "payment_info": {
            "id": 11,
            "account_number": "6228480481253312",
            "account_name": "李令",
            "opening_bank": "中国建设银行",
            "payment": {
                "key": "BANK",
                "verbose": "银行转账"
            },
            "currency": {
                "key": "RMB",
                "verbose": "人民币"
            },
            "swift_code": null
        },
        "order_payed_info": {
            "id": 32,
            "order": 118,
            "account_number": "6228451238457650123",
            "account_name": "邱雷",
            "opening_bank": "招商银行",
            "pay_date": "2017-11-15",
            "img": "http://apply.chinasummer.org/media/order/order_payment/test1.png",
            "amount": 40000
        },
        "operation_history": [      操作记录
            {
                "id": 1,
                "operator": {
                    "id": 2,
                    "name": "yirantai",
                    "role": {
                        "key": "STUDENT",
                        "verbose": "学生"
                    }
                },
                "create_time": "2017-11-16T07:23:42Z",
                "source": 123,
                "remark": "创建了订单"
            },
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```