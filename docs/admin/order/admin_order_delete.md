### 管理员删除订单

**请求地址**:
```
      GET   /admin/order/delete_order/
```

**请求参数**:
```
{
    'order' :  111    int  订单ID
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": "订单已删除",
    "field_name": ""
}
```

**失败返回**：
```

```