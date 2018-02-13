# coding: utf-8

import requests

import functools

import timeit
from tornado import concurrent


executor_pool = concurrent.futures.ThreadPoolExecutor(20)


def run_on_executor(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = executor_pool.submit(fn, *args, **kwargs)
        return future
    return wrapper


domain = "http://apply.chinasummer.org"


@run_on_executor
def test():
    url = "%s/auth/user/login/" % domain
    data = {
        "username": "StudentTest",
        "password": "123456"
    }
    res = requests.post(url=url, json=data)
    print(res.json())
    return


if __name__ == "__main__":
    print('test is start')
    for item in range(100):
        test()
    print('test is end')
