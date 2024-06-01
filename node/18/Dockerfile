FROM node:18-alpine

ARG UID
ARG GID

ENV UID=${UID:-1000}
ENV GID=${GID:-1000}

RUN mkdir -p /app
RUN mkdir -p /app-tmp

WORKDIR /app

COPY ./npm_install.sh /app-tmp/npm_install.sh
RUN chmod a+x /app-tmp/npm_install.sh

# MacOS staff group's gid is 20; so is the dialout group in alpine linux. We're not using it so let's just remove it.
RUN delgroup dialout

RUN deluser node

RUN addgroup -g ${GID} --system spark
RUN adduser -G spark --system -D -s /bin/sh -u ${UID} spark

USER spark

CMD /app-tmp/npm_install.sh \
	&& \
	npm run dev
