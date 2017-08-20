###    推广渠道详情

**请求地址**:
```
    GET     /market/channel/[channel_id]/
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
        "id": 3,
        "name": "西南财大9月推广第一期",          渠道名称
        "plan_date": "2017-08-21",             计划推广日期
        "sales_man": {
            "id": 1,
            "name": "zhangsan"
        },
        "plan_student_number": 200,            计划参加人数
        "plan_file_student_number": 100,       计划建档人数
        "plan_payed_student_number": 50,       计划缴费人数
        "create_time": "2017-08-20T14:14:57.775431Z",
        "qr_code": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQEJ8TwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyY1AxSnhBMEdjMGoxMDAwMGcwM2MAAgQupHxZAwQAAAAA"    推广二维码
    },
    "field_name": ""
}
```

**失败返回**：
```

```