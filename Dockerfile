FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /wages
WORKDIR /wages
ADD . .
RUN pip install -r requirements.txt
EXPOSE 8000
EXPOSE 8080
