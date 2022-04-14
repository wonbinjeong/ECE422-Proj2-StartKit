FROM python:3.8-alpine
ARG ENABLED=1
ADD . /code
WORKDIR /code
EXPOSE 3000
RUN pip install -r requirements.txt
CMD ["python", "-u", "app.py"]