#!/bin/bash

RC=0

if [[ $(id -ru) -eq 0 ]]
then
    
    sudo -iu postgres ./postgres-init.sh && \
    sudo -iu postgres psql -f ../sql/inv_control.sql
else
    RC=1
    echo "Script must be run as root." >&2
fi
