FROM python:3.9-alpine

RUN apk --no-cache add musl-dev linux-headers g++ 
COPY ./start.sh /start.sh
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN chmod +x /start.sh
COPY ./app /app

CMD ["./start.sh"]