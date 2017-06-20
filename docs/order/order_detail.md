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
    },
    "field_name": ""
}
```

**失败返回**：
```

```