FROM python:3.11.4

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y netcat-openbsd && apt-get install -y dos2unix && apt-get install -y nodejs npm

ENV APP=/app

# Change the workdir.
WORKDIR $APP

# Install the requirements
COPY requirements.txt $APP

RUN pip3 install -r requirements.txt

# Copy the rest of the files
COPY . $APP

# RUN chmod +x /app/entrypoint.sh
RUN dos2unix /app/entrypoint.sh

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":80", "--workers", "3", "djangobackend.wsgi"]
