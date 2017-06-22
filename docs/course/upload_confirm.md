###  上传审课图片

**请求地址**:
```
    PUT     /course/[course_id]/upload_confirm_photo/
```

**请求参数**:
```
{
    "confirm_photo": ""    base64位字符串
}
```

**成功返回**：
```
{
  "code": 0,
  "msg": "操作成功",
  "data": {},
  "field_name": ""
}
```

**失败返回**：
```

```