# Gunicorn configuration file
workers = 3
bind = "0.0.0.0:8000"
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
preload_app = True
