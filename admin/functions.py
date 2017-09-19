# coding: utf-8
from market.models import Channel


def get_channel_info(user_info_instance):
    if user_info_instance.channel_id and Channel.objects.filter(id=user_info_instance.channel_id).exists():
        channel_instance = Channel.objects.get(id=user_info_instance.channel_id)
        channel = {
            'id': channel_instance.id,
            'name': channel_instance.name,
            'create_time': channel_instance.create_time
        }
    else:
        channel_instance = Channel.objects.filter(user_channel__openid=user_info_instance.openid).first()
        if channel_instance:
            channel = {
                'id': channel_instance.id,
                'name': channel_instance.name,
                'create_time': channel_instance.create_time
            }
        else:
            channel = None

    return channel