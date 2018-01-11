# coding: utf-8

import random

from common.models import SalesManUser, SalesMan

from StuSystem.settings import DOMAIN, MEDIA_URL

TICKET_TIMEOUT = 60 * 60 * 24   # ticket过期时间 1天


def auto_assign_sales_man(user):
    """
    自动分配销售顾问
    :param user:
    :return:
    """
    sales_man = SalesMan.objects.all()
    if not sales_man:
        return dict()
    if not SalesManUser.objects.filter(user=user).exists():
        rand_int = random.randint(1, len(sales_man))
        random_sales_man = sales_man[rand_int-1]
        if DOMAIN in random_sales_man.qr_code.path:
            qr_code = random_sales_man.qr_code.path
        else:
            qr_code = '%s%s%s' % (DOMAIN, MEDIA_URL, random_sales_man.qr_code.path)
        SalesManUser.objects.get_or_create(user=user, sales_man=random_sales_man)
        res = {'id': random_sales_man.id, 'name': random_sales_man.name, 'email': random_sales_man.email,
               'qr_code': qr_code, 'wechat': random_sales_man.wechat}
    else:
        res = SalesMan.objects.filter(salesmanuser__user=user).values('id', 'name', 'email', 'qr_code', 'wechat')[0]
        res['qr_code'] = '%s%s%s' % (DOMAIN, MEDIA_URL, res['qr_code'])
    return res