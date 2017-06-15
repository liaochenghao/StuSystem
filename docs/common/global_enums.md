### 获取全局的enums

**请求地址**:
```
    GET     /common/global_enums/
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
    "user_info_gender": [                   # 用户性别信息
        {
            "key": "MALE",
            "verbose": "男"
        },
        {
            "key": "FEMALE",
            "verbose": "女"
        }
    ]
    },
"field_name": ""
}
```

**失败返回**：
```

```