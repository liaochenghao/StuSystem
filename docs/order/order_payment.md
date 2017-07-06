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
    "coupon_list": []   list  优惠券的id，coupon_list可以传空list，但coupon_list字段必填
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 1,
        "order": 31,
        "account_number": "896275756@qq.com",
        "account_name": "邱雷",
        "opening_bank": null,
        "pay_date": "2017-07-05",
        "img": "http://42.51.8.152:8002/media/order/order_payment/1%E9%A6%96%E6%AC%A1%E7%99%BB%E5%BD%95-2-%E5%A1%AB%E5%86%99%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99%E9%A1%B5%E9%9D%A2.jpg"
    },
    "field_name": ""
}
```

**失败返回**：
```

```