###  通知消息接口

**请求地址**:
```
    GET     /common/auto_notice/
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
            "module_name": "order"  模块名称,
            "user_id": 2,
            "read": false,
            "msg": "您有一条订单待支付，订单号为:5",
            "id": "5a72db35b41cae1e20859bb1",
            "create_time": "2018-2-1T9:17:38Z"
        }
    ],
    "field_name": ""
}
```
模块名称备注:
    order--订单模块，
    project--项目模块,
    course--课程模块,
    course_confirm--审课模块,
    scores--成绩模块,
    credit_switch--学分转换
```
```

**失败返回**：
```

```