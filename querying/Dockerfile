FROM node:13

RUN npm install -g ts-node typescript

# Not running as root.
ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 /usr/local/bin/dumb-init
RUN chmod +x /usr/local/bin/dumb-init

WORKDIR /app

# Add user so we don't need --no-sandbox.
RUN groupadd -r c3junior && useradd -r -g c3junior -G audio,video c3junior \
    && mkdir -p /home/c3junior \
    && chown -R c3junior:c3junior .

# Run everything after as non-privileged user.
USER c3junior

COPY ./package.json .
COPY ./yarn.lock .

RUN yarn install

COPY . .

ENV LISTEN_PORT 4000
EXPOSE 4000
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "./src/index.js"]