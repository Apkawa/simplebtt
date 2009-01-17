#!/bin/bash
#python manage.py runfcgi daemonize=false method=threaded socket=/tmp/simplebtt.sock  # < это кавайнее

#python manage.py runfcgi daemonize=false socket=/tmp/simplebtt.sock maxrequests=1

#python manage.py runfcgi method=prefork socket=/tmp/simplebtt.sock pidfile=/tmp/simplebtt.pid daemonize=false

python manage.py runfcgi method=threaded host=127.0.0.1 port=4747 daemonize=false --setting=settings_work protocol=scgi


