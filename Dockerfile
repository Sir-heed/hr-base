################################################################################
## build version and release files
################################################################################

FROM alpine AS app_res

WORKDIR /tmp
COPY ./.git /tmp/.git


################################################################################
## build django app
################################################################################

FROM python:3.12-slim-bullseye

WORKDIR /code/
ENTRYPOINT ["/code/entrypoint.sh"]
CMD ["start_dev"]

ENV APP_UID       app
ENV APP_RUN_DIR   /var/run/${APP_UID}/
ENV PY_MODULE     app
ENV VIRTUAL_ENV   ${APP_RUN_DIR}venv
ENV PATH          ${VIRTUAL_ENV}/bin:${PATH}

COPY ./conf/docker/* /tmp/
RUN /tmp/setup.sh

COPY ./pip/* /tmp/
RUN pip install -q -f /tmp/ -r /tmp/requirements.dev.txt && \
    pip install -q -f /tmp/ -r /tmp/requirements.txt && \
    rm -rf /tmp/*

COPY                --chown=${APP_UID}:${APP_UID}  ./app             ./

