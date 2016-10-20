#!/bin/bash

set -e

CUSER="doc"
MYUID=`stat -c "%u" .`

if [[ "$MYUID" -gt '0' && "$MYUID" != `id -u ${CUSER}` ]]; then
    usermod -u ${MYUID} ${CUSER}
fi

case "$1" in
    "build")
        su-exec ${CUSER} make html ;;
    "check")
        su-exec ${CUSER} make spelling ;;
    "watch")
        while su-exec ${CUSER} inotifywait -e modify -r .; do
            su-exec ${CUSER} make html
        done
        ;;
    *)
        su-exec ${CUSER} "$@" ;;
esac
