FROM python:3.5

RUN apt-get update && apt-get -y upgrade

RUN mkdir -p /app/requirements

COPY requirements/* /app/requirements/

WORKDIR /app

RUN pip install -r requirements/local.txt

COPY . /app

WORKDIR /app/gcanvas

EXPOSE 8000
ENV DJANGO_SECRET_KEY="_uxzqd*s#i$=-7d=hd$=ke-666m-44x*z5x6!!@y_1mv&o-@v^"
ENV DJANGO_SETTINGS_MODULE=gcanvas.settings.local

#ENTRYPOINT ["gunicorn"]

#CMD ["--bind", "0.0.0.0:8000", "gcanvas.wsgi"]