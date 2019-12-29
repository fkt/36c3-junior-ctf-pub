FROM node:13

# Latest node version
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install curl
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -

RUN npm install -g ts-node typescript

# puppeteer/chrome
RUN apt-get install -y libgconf-2-4 wget --no-install-recommends
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-unstable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst ttf-freefont \
      --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge --auto-remove -y curl \
    && rm -rf /src/*.deb


# It's a good idea to use dumb-init to help prevent zombie chrome processes.
ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 /usr/local/bin/dumb-init
RUN chmod +x /usr/local/bin/dumb-init

RUN mkdir /app
WORKDIR /app
# Add user so we don't need --no-sandbox.
RUN groupadd -r pptruser && useradd -r -g pptruser -G audio,video pptruser \
    && mkdir -p /home/pptruser/Downloads \
    && chown -R pptruser:pptruser /home/pptruser \
    && chown -R pptruser:pptruser .

# Run everything after as non-privileged user.
COPY ./package.json .
RUN chown pptruser:pptruser package.json

RUN yarn install
# run puppeteer installer one more time - didn't always do it (?)
RUN yarn add puppeteer
# run tsc once, not sure if the ts-node caching is good enough...

COPY . .
RUN chown -R pptruser:pptruser .

USER pptruser

ENV LISTEN_PORT 8075
EXPOSE 8075
ENTRYPOINT ["dumb-init", "--"]
CMD ["ts-node", "surfer.ts"]
