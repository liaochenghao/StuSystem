# coding: utf-8

import random
import string
import datetime
from authentication.models import Ticket
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
        return None
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


class UserTicket(object):
    """ 用户ticket
    """
    @classmethod
    def create_ticket(cls, user):
        """ 创建ticket
        """
        ticket = 'TK-'
        ticket += ''.join(random.sample(string.digits + string.ascii_letters, 20))
        data = {
            'user': user,
            'ticket': ticket,
            'expired_time': datetime.datetime.now() + datetime.timedelta(days=1)
        }
        Ticket.objects.create(**data)
        cls.clean_timeout_ticket(user)
        return ticket

    @classmethod
    def check_ticket(cls, ticket):
        """ 校验ticket
        """
        ticket = Ticket.objects.filter(ticket=ticket).last()
        if not ticket:
            return None
        if ticket.expired_time.replace(tzinfo=None) < datetime.datetime.now():
            cls.delete_ticket(ticket)
            return None
        user = ticket.user
        return user

    @classmethod
    def delete_ticket(cls, ticket):
        """ 删除ticket
        @param ticket 被删除的ticket
        """
        Ticket.objects.filter(ticket=ticket).delete()
        return

    @classmethod
    def clean_timeout_ticket(cls, user):
        """ 清除所有过期ticket
        @param user_id 用户id
        """
        Ticket.objects.filter(user=user, expired_time__lte=datetime.datetime.now()).delete()
        return