FROM python:3.10

WORKDIR /
COPY requirements.txt /home/requirements.txt
RUN pip install --no-cache-dir -r /home/requirements.txt

COPY ./ /home/
WORKDIR /home/

ENV PYTHONPATH=/home
EXPOSE 80

CMD ["gunicorn", \
    "-c", "gunicorn_conf.py", \
    "-k", "uvicorn.workers.UvicornWorker", \
    "--access-logformat", "{\"remote_ip\":\"%(h)s\",\"request_id\":\"%({X-Request-Id}i)s\",\"response_code\":\"%(s)s\",\"request_method\":\"%(m)s\",\"request_path\":\"%(U)s\",\"request_querystring\":\"%(q)s\",\"request_timetaken\":\"%(D)s\",\"response_length\":\"%(B)s\"}", \
    "app.main:app"]
