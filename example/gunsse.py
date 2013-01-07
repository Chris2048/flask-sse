bind = "0.0.0.0:8000"
workers = 6
backlog = 2048
worker_class = "gevent"
debug = True
#daemon = True
pidfile = "/tmp/gunicorn.pid"
logfile = "/tmp/gunicorn.log"
