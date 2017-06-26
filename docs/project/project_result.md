### 项目学分转换结果

**请求地址**:
```
    GET     /course/project/project_result/
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
            "id": 2,
            "name": "北京校区一期项目",         项目名称
            "create_time": "2017-06-20T15:39:48Z",
            "project_result": {               项目学分转换结果
                "id": 1,
                "status": {                   学分转换状态
                    "key": "POSTED",
                    "verbose": "成绩单已寄出"
                },
                "post_date": "2017-06-26",    成绩单寄送时间
                "post_channel": "DHL",        快递方式
                "post_number": "25424521236"  快递单号
            }
        },
        {
            "id": 3,
            "name": "北京校区二期项目",
            "create_time": "2017-06-20T15:40:16Z",
            "project_result": null          项目学分转换结果，null表示该项目还未进入学分转换流程
        }
    ],
    "field_name": ""
}
```

**失败返回**：
```

```