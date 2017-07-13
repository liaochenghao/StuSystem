### 为学生分配优惠券

**请求地址**:
```
    POST     /coupon/user_coupon/
```

**请求参数**:
```
{
    "user": int    学生id
    "coupon": int   优惠券id
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "操作成功",
    "data": {},
    "field_name": ""
}

```

**失败返回**：
```

```