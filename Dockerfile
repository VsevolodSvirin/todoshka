FROM python:3.6
ENV PYTHONUNBUFFERED 1 \
    DJANGO_SECRET_KEY "a5a(a=wdw!2z3b4po-13&$+j#wlp_57vwtpln)hbgu%gz=s_6z"
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/