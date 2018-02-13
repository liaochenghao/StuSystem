# coding: utf-8


class MessageAutoNotice:
    """
    消息通知
    模块名称:  order--订单模块，project--项目模块, course--课程模块, course_confirm--审课模块,
              scores--成绩模块, credit_switch--学分转换
    """
    def __init__(self, **kwargs):
        self.user_id = kwargs.pop('user_id')
        self.module_name = kwargs.pop('module_name')
        self.msg = kwargs.pop('msg')
        self.read = kwargs.pop('read', False)