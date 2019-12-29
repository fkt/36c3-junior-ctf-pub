FROM python:3.8-slim-buster

RUN pip install ipython

# Not running as root.
ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 /usr/local/bin/dumb-init
RUN chmod +x /usr/local/bin/dumb-init

WORKDIR /app

# Add user so we don't need --no-sandbox.
RUN groupadd -r c3junior && useradd -r -g c3junior -G audio,video c3junior \
    && mkdir -p /home/c3junior \
    && chown -R c3junior:c3junior .

USER c3junior

COPY flag.txt .
COPY ikuchen.py .

ENV LISTEN_PORT 5656
EXPOSE 5656
ENTRYPOINT ["dumb-init", "--"]
CMD ["python", "./ikuchen.py"]