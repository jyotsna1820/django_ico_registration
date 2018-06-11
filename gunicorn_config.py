command = '/home/ve/bin/gunicorn'
pythonpath = '/home/ve/bin/python'
bind = '127.0.0.1:8000'
workers = 3
usern = 'nobody'
raw_env = [
  'ENVIRONMENT=staging',
]
