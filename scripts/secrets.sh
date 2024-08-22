#!/usr/bin/env bash

# This script can be used to generate an ".env" for local development with
# docker compose.
#
# Example:
# ./scripts/secrets.sh [--silent | -s]

function check_openssl {
    which openssl > /dev/null
}

function gen_random_string {
    openssl rand -hex 16 | tr -d "\n"
}

function gen_env {
    cat << EOF
#
# USE THIS ONLY LOCALLY
#

# ==============================================================================
# Docker settings
# ==============================================================================

# Variables in this file will be substituted into docker-compose.yml
# Save a copy of this file as ".env" and insert your own values.
#
# Verify correct substitution with:
#
#   docker compose config
#
# If variables are newly added or enabled,
# please restart the images to pull in changes:
#
#   docker compose restart {container-name}
#

# Local Development
APP_DOMAIN=hr-base.local
APP_URL=http://hr-base.local


# Default environment variables
APP_ADMIN_PASSWORD=$(gen_random_string)




# Django settings

# Django 4.2 requires at least a 50-char-length secret
DJANGO_SECRET_KEY=$(gen_random_string)$(gen_random_string)$(gen_random_string)

DEBUG_TOOLBAR_ENABLED=true
FAIL_FAST=true

EOF
}


check_openssl
RET=$?
if [ $RET -eq 1 ]; then
    echo "Please install 'openssl' >  https://www.openssl.org/"
    exit 1
fi

set -Eeuo pipefail

silent="no"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --silent | -s )
            silent="yes"
            shift
        ;;

        * )
            shift
        ;;
    esac
done





gen_env > .env