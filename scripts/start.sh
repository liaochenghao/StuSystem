#!/bin/bash
ps -aux | grep 8002 | awk '{print $2}' | xargs kill -9
gunicorn StuSystem.wsgi:application -b 0.0.0.0:8002 -w 4 -t 300 --reload
