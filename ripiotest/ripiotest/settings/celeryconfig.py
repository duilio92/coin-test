broker_url = 'pyamqp://guest@localhost//'
imports = ('transactions.tasks',)
result_backend = 'redis://127.0.0.1:6379/0'
worker_concurrency = 1
