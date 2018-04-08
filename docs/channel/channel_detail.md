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
        "id": 1,
        "name": "暑校联盟服务中心公众号",
        "plan_date": "2018-03-22",
        "sales_man": {
            "id": 22,
            "name": "Ethan"
        },
        "plan_student_number": 0,
        "plan_file_student_number": 0,
        "plan_payed_student_number": 0,
        "create_time": "2018-03-22T16:20:53",
        "channel_url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx622bf44e0bee4f2b&redirect_uri=http%3A//apply.chinasummer.org/%3Fchannel_id%3D1&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect",
        "qr_code": "http://shell.chinasummer.org/media/common/channel/channel_1.jpg",
        "all_stu_number": 50,
        "file_stu_number": 10,
        "payed_stu_number": 0
    },
    "field_name": ""
}
```

**失败返回**：
```

```