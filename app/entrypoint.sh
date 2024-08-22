#!/usr/bin/env bash
set -Eeo pipefail

function show_help {
    echo """
Commands
--------------------------------------------------------------------------------

bash | sh     : run bash
eval          : eval shell command
manage        : invoke django manage.py commands

prepare_db    : creates db and prepares data model migrations
setup_db      : creates db and data model tables


The following commands are only available locally.
Do not run them in production.

start_dev     : start django server and RQ workers and scheduler

test          : run all tests
test_lint     : run code style tests
test_py       : run python tests with coverage
test_setup    : prepare database and generate app docs

gen_docs      : generate app docs
pip_freeze    : freeze pip dependencies and write them into 'requirements.prod.txt'

--------------------------------------------------------------------------------
"""
}



function prepare_db {
    # create_db

    $MANAGE makemigrations
}


function setup_db {
    # prepare_db

    # migrate data model if needed
    $MANAGE migrate --noinput
}


function setup_admin_user {
    if [ -n "$ADMIN_PASSWORD" ]; then
        # arguments:[-e=admin@test.org] -p=secretsecret
        echo $ADMIN_USER_EMAIL
        echo $ADMIN_PASSWORD
        $MANAGE setup_admin -e="admin@test.com" -p=$ADMIN_PASSWORD

        echo "Created user admin."
    else
        echo "Missing 'ADMIN_PASSWORD' environment variable."
        exit 1
    fi
}


function pip_freeze {
    local VENV=/tmp/env
    local REQ_FILE=./conf/pip/requirements.txt
    local REQ_DATE=$(date "--utc" "--rfc-3339=seconds")

    rm -rf ${VENV}
    mkdir -p ${VENV}
    python3 -m venv ${VENV}

    ${VENV}/bin/pip install -q \
        -r ./conf/pip/requirements.dev.txt \
        -r ./conf/pip/requirements.test.txt \
        --upgrade

    touch ${REQ_FILE}

    echo "" | tee ${REQ_FILE}
    echo "# ------------------------------" | tee -a ${REQ_FILE}
    echo "# Generated automatically"      | tee -a ${REQ_FILE}
    echo "# ${REQ_DATE}" | tee -a ${REQ_FILE}
    echo "# ------------------------------" | tee -a ${REQ_FILE}
    echo "" | tee -a ${REQ_FILE}

    ${VENV}/bin/pip freeze --local | grep -v appdir | tee -a ${REQ_FILE}


    chown -Rf ${APP_UID}:${APP_UID} ${REQ_FILE}
}


function collect_static {
    $MANAGE collectstatic --noinput --clear --verbosity 0
    chown -Rf ${APP_UID}:${APP_UID} ${STATIC_ROOT}
    chmod -Rf 755 ${STATIC_ROOT}
    echo "Static content collected!"
}


function setup_django {
    setup_db
    setup_admin_user

    collect_static

}


function test_setup {
    $MANAGE collectstatic --noinput --clear --verbosity 0 --dry-run
}


function test_lint {
    flake8 --toml-config ./pyproject.toml .
    rstcheck --config=./pyproject.toml -r .
}


function test_coverage {
    export DJANGO_SETTINGS_MODULE=${DEFAULT_DJANGO_SETTINGS_MODULE}_test
    export WEBPACK_STATS_FILE=./${PY_MODULE}/tests/webpack-stats.json

    check_db
    coverage erase || true

    coverage run \
        $MANAGE test \
        --parallel \
        --noinput \
        "${@:1}"

    coverage combine --append
    coverage report -m
    coverage erase

    export DJANGO_SETTINGS_MODULE=${DEFAULT_DJANGO_SETTINGS_MODULE}
}

# --------------------------------------------------------------------------
MANAGE=./manage.py

export STATIC_URL=${STATIC_URL:-/static/}
export STATIC_ROOT=${STATIC_ROOT:-/var/www/static/}

export BACKUP_DIR=./data

DEFAULT_DJANGO_SETTINGS_MODULE=${PY_MODULE}.settings
echo ${DEFAULT_DJANGO_SETTINGS_MODULE}
export DJANGO_SETTINGS_MODULE=${DEFAULT_DJANGO_SETTINGS_MODULE}
echo ${DJANGO_SETTINGS_MODULE}
export DEBUG=
export ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
# --------------------------------------------------------------------------


case "$1" in

    bash | sh )
        bash
    ;;

    eval )
        eval "${@:2}"
    ;;

    manage )
        $MANAGE "${@:2}"
        # required to change migration files owner
        chown -Rf ${APP_UID}:${APP_UID} *
    ;;

    prepare_db )
        prepare_db
    ;;

    setup_db )
        setup_db
    ;;









    # --------------------------------------------------------------------------
    # DEVELOPMENT mode
    # --------------------------------------------------------------------------

    start_dev )
        setup_django

        export DEBUG=true

        $MANAGE runserver 0.0.0.0:${PORT:-8000}
    ;;

    gen_docs )
        gen_sphinx_docs
    ;;

    pip_freeze )
        pip_freeze || true
    ;;

    # --------------------------------------------------------------------------
    # TESTS
    # --------------------------------------------------------------------------

    test )
        # Linting tasks first
        test_lint

        # Run python tests
        test_coverage "${@:2}"

        test_setup
    ;;

    test_lint )
        test_lint
    ;;

    test_py )
        test_coverage "${@:2}"
    ;;

    test_setup )
        test_setup
    ;;


    # Otherwise
    * )
        show_help
    ;;

esac
