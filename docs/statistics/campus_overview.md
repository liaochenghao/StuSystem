### 学生情况概览

**请求地址**:
```
    GET    /admin/statistics/campus_overview/
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
            "name": "北京校区",
            "info": "123",
            "create_time": "2017-06-14T23:40:30Z",
            "project_set": [
                {
                    "id": 2,
                    "name": "北京校区一期项目",
                    "applyed_number": 1,            项目申请人数
                    "payed_number": 1               项目支付人数
                },
            ]
        },
    "field_name": ""
}
```

**失败返回**：
```

```