FROM tiangolo/uwsgi-nginx-flask:python3.9

# disable nginx access log
RUN rm /var/log/nginx/access.log

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

RUN chown nobody:nogroup /app
