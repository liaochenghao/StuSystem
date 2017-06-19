### 获取校区列表

**请求地址**:
```
    GET     /coupon/add_coupon/
```

**请求参数**:
```
{
    "code": ****,                     str   代码
    "amount": 10,                   float   金额
    "info": null,               str   描述
    "start_time": 2017-1-1,                     date   开始时间
    "end_time": 2017-12-31,                   date   结束时间
    "max_num": 100,               int   总数
    "is_active": true,                     bool   时候激活
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功"
}
```

**失败返回**：
```

```