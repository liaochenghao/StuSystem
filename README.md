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
- field_name: `str`  code为非0状态时，报错字段

```
备注：
    1、接口文档中的[instance_id]为一int值，调用时需按需转换，防止调用接口时直接复制，引起错误。
        示例： ／auth／user／info／[user_id]/ 调用时需转换为  ／auth/user/info/1／

    2、 当接口文档中写了字段最小长度和最大长度时，前端输入框应做相应字符限制，以免不必要的重复开发。

    3、 本文档中返回的时间均为utc时间字符串，客户端需做+8小时转换
        示例：create_time: "2017-06-14T23:40:30Z" 转换为显示时间为： "2017-06-15 7:40:30"

    4、 本文档中列表接口默认分页，每页10条，若有特殊分页条数，在具体文档中详细说明。

    5、 获取全局的enums接口，用于获取需要用户填写时的所有可选项，增加前后端交互的灵活度。
     示例： 若要填写用户的性别，只需要调用该接口，找到user_info_gender的key对应的value，即可获得所有的备选项，
     根据用户的选择将相应的key值传给后端即可。详见接口文档

```

### API接口文档

**通用接口**:
- [获取全局的enums](docs/common/global_enums.md)
- [管理后台导航菜单栏](docs/common/desktop_navigation.md)



**用户模块**：
- [登录接口](docs/authentication/user_login.md)
- [检查用户账户信息](docs/authentication/check_account.md)
- [获取用户信息(***)](docs/authentication/user_info.md)
- [更新用户信息(***)](docs/authentication/update_user_info.md)
- [获取用户档案信息](docs/authentication/user_personal_file.md)
- [更新用户档案信息](docs/authentication/update_personal_file.md)
- [创建用户成绩邮寄信息](docs/authentication/create_score_detail.md)
- [获取用户成绩邮寄信息列表(***)](docs/authentication/get_score_list.md)
- [获取用户成绩邮寄信息详情](docs/authentication/get_score_detail.md)
- [用户优惠券信息](docs/authentication/coupon_list.md)
- [获取销售顾问二维码](docs/authentication/sales_man.md)
- [已发送好友申请](docs/authentication/post_sales_man.md)
- [检查用户信息是否需要完善](docs/authentication/check_user_info.md)
- [微信中分配销售顾问](docs/authentication/assign_sales_man.md)

**购物车**:
- [购物车项目创建(***)](docs/shopping_chart/shopping_chart_create.md)
- [购物车项目列表(***)](docs/shopping_chart/shopping_chart_list.md)
- [购物车项目详情(***)](docs/shopping_chart/shopping_chart_detail.md)
- [购物车项目更新(***)](docs/shopping_chart/shopping_chart_update.md)
- [购物车项目删除(***)](docs/shopping_chart/shopping_chart_delete.md)

**管理员订单管理**:
- [订单列表](docs/admin/order/admin_order_list.md)
- [订单详情](docs/admin/order/admin_order_detail.md)
- [订单更新](docs/admin/order/admin_order_update.md)

**管理员支付账号设置**：
- [管理员账户设置/账户列表(***)](docs/admin/account_info/account_info_list.md)
- [管理员账户设置/账户创建(***)](docs/admin/account_info/account_info_create.md)
- [管理员账户设置/账户详情(***)](docs/admin/account_info/account_info_detail.md)
- [管理员账户设置/更新账户(***)](docs/admin/account_info/account_info_update.md)
- [管理员账户设置/删除账户(***)](docs/admin/account_info/account_info_delete.md)

**管理员销售顾问**：
- [销售顾问/销售顾问列表(***)](docs/sales_man/sales_man_list.md)
- [销售顾问/创建销售顾问(***)](docs/sales_man/sales_man_create.md)
- [销售顾问/获取销售顾问详情(***)](docs/sales_man/sales_man_detail.md)
- [销售顾问/更新销售顾问(***)](docs/sales_man/sales_man_update.md)

**管理员优惠券**：
- [优惠券/创建优惠券(***)](docs/coupon/coupon_create.md)
- [优惠券/优惠券列表(***)](docs/coupon/coupon_list.md)
- [优惠券／优惠券详情(***)](docs/coupon/coupon_detail.md)
- [优惠券/更新优惠券(***)](docs/coupon/coupon_update.md)
- [优惠券/给学生分配优惠券(***)](docs/coupon/add_coupon.md)

**管理后台接口**：
- [学生信息列表](docs/admin/user_info_list.md)
- [学生信息详情](docs/admin/user_info_detail.md)
- [添加学生备注](docs/admin/add_remark.md)
- [学生审课记录列表](docs/admin/confirm_course.md)
- [学生成绩列表](docs/admin/scores_list.md)
- [成绩单寄送地址](docs/admin/student_score_info.md)
- [更新成绩单寄送信息](docs/admin/update_student_score_info.md)
- [项目管理项目列表(分页接口)](docs/admin/project_list.md)
- [项目管理项目列表(不分页接口)](docs/admin/project_list_none_pagination.md)
- [课程管理筛选条件获取](docs/admin/user_filter_elements.md)
- [产品中心/学生情况概览](docs/statistics/students_overview.md)
- [产品中心/校区情况概览](docs/statistics/campus_overview.md)
- [成绩管理/更新课程成绩](docs/admin/user_course_update.md)
- [成绩管理/更改审课状态](docs/admin/confirm_user_course.md)
- [学分转换管理/某一学生学分转换详情](docs/admin/project_result_detail.md)
- [学分转换管理/更新学分转换](docs/admin/project_result_update.md)
- [管理员为学生分配课程](docs/admin/create_user_course.md)
- [用户上传凭证待审核数量](docs/admin/course_to_confirm_count.md)

**校区模块**:
- [创建校区(***)](docs/campus/campus_create.md)
- [获取校区列表(***)](docs/campus/campus_list.md)
- [获取校区详情(***)](docs/campus/campus_detail.md)
- [更新校区(***)](docs/campus/campus_update.md)
- [获取校区所有项目(***)](docs/campus/all_projects.md)

**项目模块**：
- [创建项目(***)](docs/project/project_create.md)
- [项目列表(***)](docs/project/project_list.md)
- [项目列表--不分页接口(***)](docs/project/project_list_none_pagination.md)
- [项目详情(***)](docs/project/project_detail.md)
- [项目更新(***)](docs/project/project_update.md)
- [单个项目关联课程(***)](docs/project/single_related_courses.md)
- [所有项目关联课程(***)](docs/project/project_related_courses.md)
- [创建项目与课程的关联(***)](docs/project/create_course_project.md)
- [设置项目课程数量及相应费用(***)](docs/project/project_course_fee.md)

**课程模块**:
- [创建课程(***)](docs/course/course_create.md)
- [课程列表(***)](docs/course/course_list.md)
- [课程列表--不分页接口(***)](docs/course/course_list_none_pagination.md)
- [课程详情(***)](docs/course/course_detail.md)
- [课程更新(***)](docs/course/course_update.md)
- [课程关联项目(***)](docs/course/course_related_projects.md)

**学生课程**:
- [学生选课(***)](docs/user_course/create_user_courses.md)
- [当前选课详情(***)](docs/course/current_courses_info.md)
- [我的成绩(***)](docs/user_course/my_scores.md)
- [学生审课(***)](docs/user_course/student_course_confirm.md)
- [学分转换](docs/user_course/course_credit_switch.md)


**订单模块**:
- [创建订单(***)](docs/order/order_create.md)
- [订单详情(***)](docs/order/order_detail.md)
- [订单列表(***)](docs/order/order_list.md)
- [上传订单支付信息(***)](docs/order/order_payment.md)
- [检查是否可以创建订单(***)](docs/order/check_order.md)
- [取消订单(***)](docs/order/update_order.md)
- [获取当前用户所有订单(***)](docs/order/user_order_list.md)
- [获取当前用户所有订单，选课信息，审课(***)](docs/order/user_order_course.md)
- [订单币种及支付方式(***)](docs/order/order_currency_payment.md)


**渠道模块**：
- [创建推广渠道](docs/channel/channel_create.md)
- [推广渠道列表](docs/channel/channel_list.md)
- [推广渠道详情](docs/channel/channel_detail.md)
- [推广渠道更新](docs/channel/channel_update.md)


**子账号模块**：
- [子账号列表](docs/child_user/child_user_list.md)
- [子账号创建](docs/child_user/child_user_create.md)
- [子账号详情](docs/child_user/child_user_detail.md)
- [子账号更新](docs/child_user/child_user_update.md)
- [修改密码](docs/child_user/password_update.md)