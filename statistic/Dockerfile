# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/statistic

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

#CMD ["uvicorn", "main:stat", "--host", "0.0.0.0", "--port", "5000"]