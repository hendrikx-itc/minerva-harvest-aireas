#!/bin/bash

if [ -d "/data/trendstore" ]; then
    if [ ! -f "/tmp/trendstoredone" ]; then
	/plugins/aireas/setup_trendstore.sh
    fi
fi

if [ -n "$1" ]; then
    DIRNAME=$1
else
    DIRNAME="~/testdata_aireas"
fi

mkdir -p $DIRNAME

wget "http://data.aireas.com/api/v2/airboxes" -O $DIRNAME/data.json
DATENUMBER=`grep -o -a -m 1 -h -r "date[^}]*" $DIRNAME/data.json | head -1 | grep -o -E '[0-9]+'`

mv $DIRNAME/data.json $DIRNAME/$DATENUMBER.json

PGDATABASE=minerva PGHOST=database PGUSER=postgres /usr/local/bin/minerva load-data --data-source aireas -p aireas -v --statistics $DIRNAME/$DATENUMBER.json
