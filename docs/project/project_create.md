### 创建项目

**请求地址**:
```
    POST   /course/project/
```

**请求参数**:
```
{
    "campus":   int    必填  校区id
    "name":     str    必填  项目名称     最大长度30
    "start_date":  str    必填  项目开始时间
    "end_date": str       必填  项目结束时间
    "address":  str       必填  上课地点     最大长度 30
    "info":     str       必填  项目描述     最大长度255
    "apply_fee":  float   选填  申请费
    "course_num": int     必填  课程数量
    "project_fees": [     必填  课程费用
			{
				"course_number": 1,
				"course_fee": 1000
			},
		]
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "id": 1,
        "campus": {             校区信息
            "id": 3,
            "name": "南京校区",
            "campus_type": {    暑校类型信息
                "id": 1,
                "title": "北美暑校",
                "create_time": "2017-06-14T23:38:14Z"
            },
            "info": "123",
            "create_time": "2017-06-14T23:41:05Z"
        },
        "name": "项目1",          str    项目名称
        "start_date": "2017-06-20",     str   开始时间
        "end_date": "2017-07-01",       str   结束时间
        "address": "长城路二段99号",      str   上课地点
        "max_num": 150,                 int    最大选课人数
        "info": "这是项目须知，详情联系18608146540",       str   项目描述
        "create_time": "2017-06-19T14:09:43Z"
        "apply_fee": 2000.0,        float  申请奋勇
        "course_num": 3             int    课程数量
    }
    "field_name": ""
}
```

**失败返回**：
```

```