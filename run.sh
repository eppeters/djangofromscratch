#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

#/ Usage: <script> APP [options]
#/ Description: Deploy to heroku, or test locally.
#/ Examples: run dfsdjango
#/ Options:
#/   NONE: With no options, the app will be deployed.
#/   --help: Display this help message
#/   -d|--dev: Run locally for development instead of deploying.
#/   -t|--tests: Run tests instead of deploying.
usage() { grep '^#/' "$0" | cut -c4- ; exit 0 ; }
expr "$*" : ".*--help" > /dev/null && usage

readonly LOG_FILE="/tmp/$(basename "$0").log"
info()    { echo "[INFO]    $@" | tee -a "$LOG_FILE" >&2 ; }
warning() { echo "[WARNING] $@" | tee -a "$LOG_FILE" >&2 ; }
error()   { echo "[ERROR]   $@" | tee -a "$LOG_FILE" >&2 ; }
fatal()   { echo "[FATAL]   $@" | tee -a "$LOG_FILE" >&2 ; exit 1 ; }

export PYENV_VIRTUALENV_DISABLE_PROMPT=1
set +euo > /dev/null
eval "$(pyenv init -)"
if pyenv commands | command grep -q virtualenv-init; then
    eval "$(pyenv virtualenv-init -)"
fi
set -euo > /dev/null

app=${1:-}
if [[ ! "$app" ]]; then
    usage
fi
shift
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -t|--test)
        is_test=true
    ;;
    -d|--dest)
        is_dev=true
    ;;
    *)
        fatal "Unknown option: $key"
    ;;
esac
shift # past argument or value
done

eval_app_cmd() {
    pushd "$1"
    set +euo > /dev/null
    pyenv activate
    set -euo > /dev/null
    info "Activated virtualenv: $PYENV_VIRTUAL_ENV"
    eval "$2"
    return_val=$?
    popd
    exit $return_val
}

if [[ "${BASH_SOURCE[0]}" = "$0" ]]; then
    if ${is_dev:-false}; then
        eval_app_cmd "$app" "heroku local -f Procfile.dev"
    fi
    if ${is_test:-false}; then
        eval_app_cmd "$app" "pytest tests/"
    fi
    heroku config:set DISABLE_COLLECTSTATIC=1 -a "$app"
    git subtree push --force --prefix "$app" "heroku-$app" master
fi
