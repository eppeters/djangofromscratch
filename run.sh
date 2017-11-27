#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

#/ Usage: <script> APP
#/ Description: Deploy to heroku, or test locally.
#/ Examples: run dfsdjango
#/ Options:
#/   --help: Display this help message
#/   -t|--test: Run locally instead of deploying.
usage() { grep '^#/' "$0" | cut -c4- ; exit 0 ; }
expr "$*" : ".*--help" > /dev/null && usage

readonly LOG_FILE="/tmp/$(basename "$0").log"
info()    { echo "[INFO]    $@" | tee -a "$LOG_FILE" >&2 ; }
warning() { echo "[WARNING] $@" | tee -a "$LOG_FILE" >&2 ; }
error()   { echo "[ERROR]   $@" | tee -a "$LOG_FILE" >&2 ; }
fatal()   { echo "[FATAL]   $@" | tee -a "$LOG_FILE" >&2 ; exit 1 ; }

# Use -gt 1 to consume two arguments per pass in the loop (e.g. each
# argument has a corresponding value to go with it).
# Use -gt 0 to consume one or more arguments per pass in the loop (e.g.
# some arguments don't have a corresponding value to go with it such
# as in the --default example).
# note: if this is set to -gt 0 the /etc/hosts part is not recognized ( may be a bug )
app=$1
shift
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -t|--test)
    is_test=true
    ;;
    *)
        fatal "Unknown option: $key"
    ;;
esac
shift # past argument or value
done

if [[ "${BASH_SOURCE[0]}" = "$0" ]]; then
    if ${is_test:-false}; then
        cmd="heroku local"
        pushd "$app"
        eval "$cmd"
        popd
        exit
    fi

    git subtree push --prefix "$app" "heroku-$app" master
fi
