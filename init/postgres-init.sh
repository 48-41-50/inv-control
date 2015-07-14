#!/usr/bin/bash


function GetBinaryPath()
{
    local PG_PATH=''
    
    # Verify path to binary files
    PG_PATH=$(find /usr -name 'pg_ctl' 2>/dev/null | head -1)
    
    if [[ -n "${PG_PATH}" ]]
    then
        PG_PATH=${PG_PATH%/*}
    else
        printf "Enter the path to the PostgreSQL binary files: "
        read PG_PATH
    fi
    
    echo $PG_PATH
}


function AddPGPath()
{
    local PG_PATH=$1
    
    cat <<EOF >>.pgsql_profile
PATH=${PG_PATH}:${PATH}
export PATH
EOF
    if ! grep -q '.pgsql_profile' .bash_profile
    then
        cat <<EOF >>.bash_profile

[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile
EOF
    fi
    
    source .bash_profile
}


function AddPGData()
{
    local RC=0
    local PGDATA=''
    local PG_PATH=$(GetBinaryPath)
    local PG_VER_PATT='([[:digit:]]{1,}\.[[:digit:]]{1,})'
    local PG_VERSION=''
    
    [[ $PG_PATH =~ $PG_VER_PATT ]]
    PG_VERSION=${BASH_REMATCH[1]}
    PGDATA=$(pwd)
    [[ -n "${PG_VERSION}" ]] && PGDATA=${PGDATA}/${PG_VERSION}
    PGDATA=${PGDATA}/pgdata
    
    mkdir -p ${PGDATA} && \
    cat <<EOF >>.pgsql_profile

PGDATA=${PGDATA}
export PGDATA
EOF
    
    RC=$?
    
    source .bash_profile
    
    return $RC
}


function VerifyBinaryPath()
{
    local PG_CTL=pg_ctl
    local PG_PATH=$(GetBinaryPath)
    local PG_PATH_LEN=${#PG_PATH}
    local TEST_PATH_LEN=0
    local RC=3
    
    if [[ -n "${PG_PATH}" ]]
    then
        if [[ -r ${PG_PATH}/${PG_CTL} && -x ${PG_PATH}/${PG_CTL} ]]
        then
            # Path verified! See if it is in the PATH env var
            TEST_PATH_LEN=$(expr ${PATH} : ${PG_PATH})
            if [[ ${TEST_PATH_LEN} -ne ${PG_PATH_LEN} ]]
            then
                AddPGPath "${PG_PATH}"
            fi
        else
            printf "Could not locate PostgreSQL binary files. Contact your administrator." >&2
            RC=2
        fi
    else
        printf "Could not locate PostgreSQL binary file path. Contact your administrator." >&2
        RC=1
    fi
    
    return $RC
}


function VerifyPGData()
{
    local RC=0
    
    if [[ -z "${PGDATA}" ]]
    then
        AddPGData
        RC=$?
    fi
}


function VerifyServer()
{
    local RC=0
    
    if $(ls -1 ${PGDATA} | wc -l) -eq 0
    then
        initdb $PGDATA && \
        cd $PGDATA && \
        tar cvf orig_conf.tar ./*.conf && \
        cd - && \
        sed --in-place -e 's/   trust/   md5/g' $PGDATA/pg_hba.conf && \
        sed --in-place -e 's/local *all *all *md5/local   all             postgres                                trust/1' $PGDATA/pg_hba.conf && \
        echo 'local   all             all                                     md5' >>$PGDATA/pg_hba.conf
        
        RC=$?
    fi
    
    if [[ $RC -eq 0 ]]
    then
        if ! pg_ctl -D $PGDATA status >/dev/null
        then
            pg_ctl start -D $PGDATA
            
            RC=$?
        fi
    fi
    
    return $RC
}


if [[ "$(id -un)" == "postgres" ]]
then
    VerifyBinaryPath
    VerifyPGData
    VerifyServer
    
    exit $?
fi
