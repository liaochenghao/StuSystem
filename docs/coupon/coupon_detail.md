###   优惠券详情

**请求地址**:
```
    GET     /coupon/coupon/[coupon_id]/
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
        "id": 3,
        "coupon_code": "HGENY0X93M",
        "amount": 2000.0,
        "info": "北京大学专属优惠券",
        "start_time": "2017-07-12T16:00:00Z",
        "end_time": "2017-07-30T16:00:00Z",
        "max_num": 30,
        "create_time": "2017-07-13T14:33:33Z",
        "is_active": true
    },
    "field_name": ""
}
```

**失败返回**：
```

```