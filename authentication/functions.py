# coding: utf-8

import random
import string
import datetime
from .models import Ticket

TICKET_TIMEOUT = 60 * 60 * 24   # ticket过期时间 1天


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