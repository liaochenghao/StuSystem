###  创建推广渠道

**请求地址**:
```
    POST    /market/channel/
```

**请求参数**:
```
{
    "name":  str 渠道名称  必填  最大长度30
    "plan_date": date 计划推广日期  必填
    "sales_man": int   销售人员id   必填
    "plan_student_number"： int  预计参加人数  必填
    "plan_file_student_number"： int  预计建档人数  必填
    "plan_payed_student_number"  int  预计缴费人数   必填
}
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