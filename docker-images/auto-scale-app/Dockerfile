FROM python:3.8-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 7000
CMD ["python", "-u", "app.py"]