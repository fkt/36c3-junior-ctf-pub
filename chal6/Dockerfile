FROM ubuntu:18.04 as base

COPY flag /

RUN apt -y update && \
    apt -y install python2.7 python-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip install jinja2 flask gunicorn
RUN groupadd -r c3junior && useradd -r -g c3junior -G audio,video c3junior \
    && mkdir /app \
    && chown -R c3junior:c3junior /app

USER c3junior

COPY wsgi.py project.py /app/
COPY templates/home.html /app/templates/home.html

WORKDIR /app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
