FROM python:3.10

MAINTAINER Daniel Reeves "xdanielreeves@gmail.com"

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
    "app.main:app"]
