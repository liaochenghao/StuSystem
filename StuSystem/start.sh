#!/bin/bash
ps -aux | grep 9002 | awk '{print $2}' | xargs kill -9
python manage.py runserver 0.0.0.0:8000