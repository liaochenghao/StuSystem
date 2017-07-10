### 获取订单 详情


**请求地址**:
```
    GET   /order/[order_id]/
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
        "id": 1,
        "user": 1,          用户id
        "project": {        项目信息
            "id": 2,
            "campus": {     校区信息
                "id": 1,
                "name": "北京校区",
                "campus_type": {
                    "id": 1,
                    "title": "北美暑校",
                    "create_time": "2017-06-14T23:38:14Z"
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
            "apply_fee": 1000.0,
            "course_num": 3
        },
        "currency": {           支付币种
            "key": "DOLLAR",
            "verbose": "美金"
        },
        "payment": {           支付方式
            "key": "ON_LINE",
            "verbose": "线上支付"
        },
        "create_time": "2017-06-20T16:31:39Z",
        "status": {            支付状态
            "key": "TO_PAY",
            "verbose": "待支付"
        },
        "standard_fee": 1000.0, 标准费用
        "pay_fee": 800.0        支付费用
        "course_num": 3,        课程数量
        "remark": ""            订单备注
        "payment_info": {
            "id": 1,
            "account_number": "896275756@qq.com",        转账账号
            "account_name": "qiulei",                    账户姓名
            "opening_bank": null,                        开户银行，可能为空
            "payment": {
                "key": "ALI_PAY",
                "verbose": "支付宝转账"
            }
        },
        "order_payed_info": {
            "id": 2,
            "order": 34,
            "account_number": "yirantai@hotmail.com",
            "account_name": "邱雷",
            "opening_bank": null,
            "pay_date": "2017-07-06",
            "img": null
        }，
        "user_course": [
                    {
                        "id": 2,
                        "name": "大学通识课一",
                        "course_code": "6ZDGW28OL7"
                    },
                ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```