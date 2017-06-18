### 用户优惠券信息

**请求地址**:
```
    GET     /auth/user/[user_id]/coupon_list/
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
    "data": [
        {
            "id": 1,
            "code": "8AD51",        str     # 优惠码
            "amount": 1000,         int     # 优惠金额
            "info": "申请I阶段优惠",  str     # 优惠说明
            "start_time": "2017-06-18T16:40:49Z",       str  # 优惠券开始时间
            "end_time": "2017-06-29T16:40:53Z"          str  # 优惠券结束时间
        },
    ],
    "field_name": ""
}
```

**失败返回**：
```

```