### 学生情况概览

**请求地址**:
```
    GET    /admin/statistics/students_overview/
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
    "data": {
        "students_num": 6,          学生人数
        "personal_file_num": 3,     已建档人数
        "students_applyed": 2,      已申请人数
        "students_payed": 1         已支付人数
    },
    "field_name": ""
}
```

**失败返回**：
```

```