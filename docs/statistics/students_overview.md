### 学生情况概览

**请求地址**:
```
    GET    /admin/statistics/students_overview/
```

**请求参数**:
```
    "create_year"  int 选填（根据年限筛选统计）
    
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": [
        {
            "key": "ALL_STUDENTS",
            "verbose": "全部学生",
            "number": 912
        },
        {
            "key": "NEW",
            "verbose": "新建用户",
            "number": 413
        },
        {
            "key": "PERSONAL_FILE",
            "verbose": "已建档",
            "number": 172
        },
        {
            "key": "ADDED_CC",
            "verbose": "已添加CC",
            "number": 44
        },
        {
            "key": "SUPPLY_ORDER",
            "verbose": "已提交订单",
            "number": 152
        },
        {
            "key": "PAYMENT_CONFIRM",
            "verbose": "待缴费确认",
            "number": 94
        },
        {
            "key": "TO_CHOOSE_COURSE",
            "verbose": "待选课",
            "number": 28
        },
        {
            "key": "PICKUP_COURSE",
            "verbose": "已选课",
            "number": 6
        },
        {
            "key": "TO_CONFIRMED",
            "verbose": "待审课确认",
            "number": 1
        },
        {
            "key": "CONFIRMED_COURSE",
            "verbose": "已审课",
            "number": 0
        },
        {
            "key": "AFTER_SCORE",
            "verbose": "已出成绩",
            "number": 0
        },
        {
            "key": "SWITCH_CREDIT",
            "verbose": "学分转换中",
            "number": 1
        },
        {
            "key": "SWITCHED_COURSE",
            "verbose": "已学分转换",
            "number": 0
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```