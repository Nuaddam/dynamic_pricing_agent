# worker.py

import os

from uvicorn.workers import UvicornWorker


class UvicornAsyncioWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "asyncio", "http": "auto"}


class UvicornUvloopWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "auto"}


# # For macOS, uncomment the following line to disable fork safety
# os.environ.setdefault("OBJC_DISABLE_INITIALIZE_FORK_SAFETY", "YES")

wsgi_app = "app.main:app"
timeout = 0
preload = True
worker_class = "uvicorn.workers.UvicornWorker"
_port = os.environ.get("PORT", "8000")
bind = f"[::]:{_port}"
if os.getenv("ENV", "dev") == "dev":
    workers = 1
    threads = 1
else:
    cpu_count = os.cpu_count()
    workers = cpu_count  # Multiple workers to handle concurrent requests
    threads = cpu_count * 2  # multiply by [2, 4]

print(f"Gunicorn workers: {workers}, threads: {threads}, port: {_port}")
