FROM python:3.10-alpine

ENV VENV_PATH=/workspace/
ENV PROJECT_PATH=/workspace/5_rest_api
ENV DIR=/workspace/
RUN apk update
RUN apk add git \
    openssh \
    github-cli
WORKDIR /usr/local/bin
COPY docker-entrypoint.sh .
RUN chmod a+x docker-entrypoint.sh
RUN sed -i 's/\r$//' docker-entrypoint.sh \
    && sed -i '1s/^\xEF\xBB\xBF//' docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]