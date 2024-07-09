FROM node:16-alpine

RUN mkdir -p /app
RUN mkdir -p /app-tmp

WORKDIR /app

COPY ./npm_install.sh /app-tmp/npm_install.sh
RUN chmod a+x /app-tmp/npm_install.sh

CMD /app-tmp/npm_install.sh \
	&& \
	npm run dev
