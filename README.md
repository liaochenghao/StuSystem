# 后台接口文档


## 测试服务地址
- http://42.51.8.152:8002


### 数据返回格式

**统一为 `json` 格式**:
```
    {
        "code": 0,
        "msg": "success",
        "data": {
            ... // 数据内容
        }
        field_name: ""
    }
```
- code `int` 0为成功，非0为失败 (code=401表示未登录)
- msg `string` 成功或失败的消息
- data `dict` 返回的数据内容
- field_name: ""  code为非0状态时，报错字段

```
备注：
    1、接口文档中的[instance_id]为一int值，调用时需按需转换，防止调用接口时直接复制，引起错误。
        示例： ／auth／user／info／[user_id]/ 调用时需转换为  ／auth/user/info/1／

    2、 当接口文档中写了字段最小长度和最大长度时，前端输入框应做相应字符限制，以免不必要的重复开发。

```

### API接口文档

**通用接口**:


**用户模块**：
- [登录接口](docs/authentication/user_login.md)      # 用户管理员网页登录
- [检查用户账户信息](docs/authentication/check_account.md)
- [获取用户信息](docs/authentication/user_info.md)