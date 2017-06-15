# coding: utf-8


def get_key_verbose_data(data: dict):
    """将dict数据结构变为key,verbose的list"""
    res = []
    for key, value in data.items():
        res.append({'key': key, 'verbose': value}),
    return res