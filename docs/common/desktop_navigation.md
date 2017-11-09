### 管理后台导航菜单栏获取

**请求地址**:
```
    GET     /common/navigation/
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
            "name": "咨询中心",
            "key": "CONSULTATON_CENTER",
            "second_levels": [
                {
                    "id": 1,
                    "name": "学生列表",
                    "key": "STUDENT_LIST"
                }
            ]
        },
        {
            "id": 2,
            "name": "财务中心",
            "key": "FINANCIAL_CENTER",
            "second_levels": [
                {
                    "id": 2,
                    "name": "首页",
                    "key": "INDEX_PAGE"
                }
            ]
        },
        {
            "id": 3,
            "name": "产品中心",
            "key": "PRODUCT_CENTER",
            "second_levels": [
                {
                    "id": 3,
                    "name": "首页",
                    "key": "INDEX_PAGE"
                },
                {
                    "id": 4,
                    "name": "学生管理",
                    "key": "SUTDENT_MANAGEMENT"
                },
                {
                    "id": 5,
                    "name": "课程管理",
                    "key": "COURSE_MANAGEMENT"
                },
                {
                    "id": 6,
                    "name": "暑校类型管理",
                    "key": "CAMPUS_TYPE_MANAGEMENT"
                },
                {
                    "id": 7,
                    "name": "暑校国家管理",
                    "key": "CAMPUS_COUNTRY_MANAGEMENT"
                },
                {
                    "id": 8,
                    "name": "校区管理",
                    "key": "CAMPUS_MANAGEMENT"
                },
                {
                    "id": 9,
                    "name": "项目管理",
                    "key": "PROJECT_MANAGEMENT"
                },
                {
                    "id": 10,
                    "name": "销售顾问",
                    "key": "SALES_MAN_MANAGEMENT"
                },
                {
                    "id": 11,
                    "name": "优惠券",
                    "key": "COUPON_MANAGEMENT"
                }
            ]
        },
        {
            "id": 4,
            "name": "市场",
            "key": "MARKET_CENTER",
            "second_levels": [
                {
                    "id": 12,
                    "name": "渠道管理",
                    "key": "CHANNEL_MANAGEMENT"
                }
            ]
        },
        {
            "id": 5,
            "name": "系统中心",
            "key": "SYSTEM_CENTER",
            "second_levels": [
                {
                    "id": 13,
                    "name": "账户管理",
                    "key": "BANK_ACCOUNT_MANAGEMENT"
                },
                {
                    "id": 14,
                    "name": "用户管理",
                    "key": "CHILD_USER_MANAGEMENT"
                }
            ]
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```