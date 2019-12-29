FROM ubuntu:18.04 as base

COPY bottle.py run.py /app/
COPY flag /

RUN apt -y update && \
    apt -y install python2.7 python-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip install Paste
CMD ["python2.7", "/app/run.py"]
