FROM python:3.10

WORKDIR /app

ADD requirements.txt /app/

RUN pip3 install -r requirements.txt

ADD ./ /app/

EXPOSE 9999
CMD ["/bin/bash","-c","python3 app.py"]