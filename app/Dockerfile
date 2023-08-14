FROM python:3.6-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. 
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
#CMD exec gunicorn --bind :80 --workers 1 --threads 8 --timeout 0 main:app

# Run app.py using gunicorn when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]