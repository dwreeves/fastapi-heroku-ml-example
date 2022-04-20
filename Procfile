# ==============================================================================
# This file is used to deploy the website to Heroku
#
# See here for more:
# https://devcenter.heroku.com/articles/procfile
# ==============================================================================

release: alembic upgrade head

web: gunicorn -c "gunicorn_conf.py" -k "uvicorn.workers.UvicornWorker" "app.main:app"

worker: celery -A "app.celery:celery_app" worker
