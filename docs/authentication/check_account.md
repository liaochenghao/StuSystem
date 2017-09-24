### 检查用户账户信息

**请求地址**:
```
    GET  ／auth/user/check_account/
```

**请求参数**:
```
{
    "code": ""      str     # 微信网页授权返回的code
}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "need_complete_student_info"： True   Boolean        # 是否需要完善用户信息,
        "valid_sales_man": True   Boolean   # 学生是否添加销售顾问微信
        "user_id":  int    # 当前用户的id
        "ticket":   str
    }
}
```

```
备注： 此接口微信网页授权后，会默认创建用户。并检测用户信息是否完整。need_complete_stu_info为True表示用户信息不完整,
    需调相关接口完善用户的信息。
```


**失败返回**：
```

```