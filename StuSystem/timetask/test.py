# coding: utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import datetime


def time_task_1(url):
    print('running time_task...')
    res = requests.post(url, json={'username': 'AdminUser', 'password': 'test123456'})
    print('done,res: %s' % res.json())


def time_task_2():
    print('this is a test')


if __name__ == '__main__':
    # url = 'http://127.0.0.1:8002/auth/user/login/'
    # print('time task init....')
    # sched = BlockingScheduler()
    # job = sched.add_job(time_task_1,
    #                     'date',
    #                     run_date=datetime.datetime.now(),
    #                     args=[url])
    #
    # sched.start()
    # job.remove()
    # print('closed time_task_1')
    #
    # print('start time_task_2')
    #
    # job_2 = sched.add_job(time_task_2,
    #                       'date',
    #                       run_date=datetime.datetime.now(),
    #                       args=[])
    # sched.start()
    # job_2.remove()
    # print('closed time_task_2')

    time_task_2()