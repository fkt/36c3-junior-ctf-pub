FROM python:3.8-buster

RUN apt -y update && \
    apt -y install python3 python-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip install flask gunicorn
RUN groupadd -r c3junior && useradd -r -g c3junior -G audio,video c3junior \
    && mkdir /app \
    && chown -R c3junior:c3junior /app 
 
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

USER c3junior

COPY . .

EXPOSE 8010
CMD ["gunicorn", "--bind", "0.0.0.0:8010", "--workers", "11", "--access-logfile", "-", "noncechallpass:app"]