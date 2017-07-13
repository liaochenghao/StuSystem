###    优惠券列表

**请求地址**:
```
    GET    /coupon/coupon/
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
        "count": 3,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "coupon_code": "HGENY0X92N",       优惠码
                "amount": 200.0,            优惠金额
                "info": "申请I阶段优惠",      优惠说明
                "start_time": "2017-06-18T16:40:49Z",
                "end_time": "2017-06-29T16:40:53Z",
                "max_num": 30,              最大数量
                "create_time": "2017-06-18T16:55:16Z",
                "is_active": true
            },
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```