#!/usr/bin/env bash
set -Eeuo pipefail

POSTGRES_PACKAGE=postgresql-client-16
APT_INSTALL="apt-get -qq --yes --allow-downgrades --allow-remove-essential --allow-change-held-packages install"


################################################################################
# install packages
################################################################################

# install missing packages of slim distribution and app required ones
PACKAGE_LIST=/tmp/apt-packages.txt
if [ -f "${PACKAGE_LIST}" ]; then
    apt-get update -qq > /dev/null
    # shellcheck disable=SC2046
    ${APT_INSTALL} $(cat ${PACKAGE_LIST}) > /dev/null
fi

# add postgres apt repo to get more recent postgres versions
echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/postgresql.gpg
apt-get update -qq > /dev/null
${APT_INSTALL} ${POSTGRES_PACKAGE} > /dev/null

# setup python environment
mkdir -p "${VIRTUAL_ENV}"
python3 -m venv "${VIRTUAL_ENV}"
pip install -q --upgrade pip
pip install -q --upgrade setuptools


################################################################################
# Create user and folders
################################################################################

useradd -s /bin/false "${APP_UID}"

mkdir -p "${APP_RUN_DIR}/log/"
touch    "${APP_RUN_DIR}/uwsgi.pid"

# shellcheck disable=SC2086
chmod -Rf 755 ${APP_RUN_DIR}/*
# shellcheck disable=SC2086
chown -Rf "${APP_UID}":"${APP_UID}" ${APP_RUN_DIR}/*
chown -Rf "${APP_UID}":"${APP_UID}" ./* || true


################################################################################
# cleaning
################################################################################

apt-get -qq --yes clean      > /dev/null
apt-get -qq --yes autoclean  > /dev/null
apt-get -qq --yes autoremove > /dev/null
