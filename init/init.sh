#!/bin/bash

RC=0

if [[ $(id -ru) -eq 0 ]]
then
    declare ADMIN_DB_PW=$(echo "$$$(date '+%S')" | ccrypt -efK $(date '+%s') | base64)
    sleep 1
    declare USER_DB_PW=$(echo "$$$(date '+%S')" | ccrypt -efK $(date '+%s') | base64)
    sleep 1
    declare ROOT_APP_PW=$(echo "$$$(date '+%S')" | ccrypt -efK $(date '+%s') | base64)
    
    sudo -iu postgres ./postgres-init.sh && \
    sed -e 's/{ADMIN_ENC_PW}/${ADMIN_DB_PW}/g' \
        -e 's/{USER_ENC_PW}/${USER_DB_PW}/g' \
        -e 's/{ROOT_PASSWORD}/${ROOT_APP_PW}/g' \
        ../sql/inv_control.sql \
        >./inv_control.sql && \
    sudo -iu postgres psql -f ./inv_control.sql && \
    unlink ./inv_control.sql
    RC=$?
else
    RC=1
    echo "Script must be run as root." >&2
fi

exit $RC
