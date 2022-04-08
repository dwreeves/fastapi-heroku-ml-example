import multiprocessing
import os


def gen_config():
    loglevel = os.getenv("LOG_LEVEL", "info")

    _workers_per_core = int(os.getenv("WORKERS_PER_CORE", "2"))
    workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * _workers_per_core))

    threads = int(os.getenv("PYTHON_MAX_THREADS", 1))

    keepalive = 120

    errorlog = "-"
    accesslog = "-"

    _host = os.getenv("HOST", "0.0.0.0")
    _port = os.getenv("PORT", "80")
    bind = os.getenv("BIND", f"{_host}:{_port}")

    return {k: v for k, v in locals().items() if not k.startswith("_")}


cfg = gen_config()
padding = max([len(i) for i in cfg.keys()])

print("Gunicorn config:")
for k, v in cfg.items():
    print(f"{k.ljust(padding)} = {v!r}")

globals().update(cfg)
