import multiprocessing
import sys
import os
sys.path.append('./')

app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

backlog = 2048
keepalive = 300
worker_class = "uvicorn.worker.UvicornWorker"
worker_connections = 50
max_requests = 20480
timeout = 1200  # master force kill children if children are unresponsive after this time
graceful_timeout = 60  # master force kill children after 300s when restarting
daemon = False
limit_request_line = 0
preload_app = False

user = 'root'
group = 'root'
workers = multiprocessing.cpu_count() * 2 + 1
errorlog = '-'
loglevel = "info"
bind = '0.0.0.0:8001'


def post_fork(server, worker):
	import random
	random.seed()
