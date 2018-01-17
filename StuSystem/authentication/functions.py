# coding: utf-8

import random

from common.models import SalesManUser, SalesMan

from StuSystem.settings import DOMAIN, MEDIA_URL
from market.models import Channel


def auto_assign_sales_man(user):
    """
    自动分配销售顾问，
    如果用户进入时存在渠道信息，则将该渠道的销售人员直接分配给该用户。
    如果该用户存在推荐给他的用户(A)，则将推荐给他人(A)的销售顾问分配给该用户。
    :param user:
    :return:
    """
    sales_man_all = SalesMan.objects.all()
    if not sales_man_all:
        return dict()
    if not SalesManUser.objects.filter(user=user).exists():
        if user.channel_id:
            # 如果用户进入时存在渠道信息
            sales_man = Channel.objects.get(id=user.channel_id).sales_man
        elif user.recommend_user:
            # 如果该用户存在推荐给他的用户(A)
            recommend_user_salesman = SalesManUser.objects.filter(user=user.recommend_user).first()
            if recommend_user_salesman:
                sales_man = recommend_user_salesman.sales_man
            else:
                rand_int = random.randint(1, len(sales_man_all))
                sales_man = sales_man_all[rand_int - 1]
        else:
            rand_int = random.randint(1, len(sales_man_all))
            sales_man = sales_man_all[rand_int-1]

        if DOMAIN in sales_man.qr_code.path:
            qr_code = sales_man.qr_code.path
        else:
            qr_code = '%s%s%s' % (DOMAIN, MEDIA_URL, str(sales_man.qr_code))
        SalesManUser.objects.create(user=user, sales_man=sales_man)
        res = {'id': sales_man.id, 'name': sales_man.name, 'email': sales_man.email,
               'qr_code': qr_code, 'wechat': sales_man.wechat}
    else:
        res = SalesMan.objects.filter(salesmanuser__user=user).values('id', 'name', 'email', 'qr_code', 'wechat')[0]
        res['qr_code'] = '%s%s%s' % (DOMAIN, MEDIA_URL, res['qr_code'])
    return res