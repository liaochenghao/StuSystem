###  通知消息接口

**请求地址**:
```
    PUT     /common/auto_notice/
```

**请求参数**:
```
    {
        "module_name": str  模块名称  必填
    }

模块名称备注:
    order--订单模块，
    project--项目模块,
    course--课程模块,
    course_confirm--审课模块,
    scores--成绩模块,
    credit_switch--学分转换
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [],
    "field_name": ""
}
```

**失败返回**：
```

```