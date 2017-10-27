#!/bin/bash

wget "http://data.aireas.com/api/v2/airboxes" -O ~/testdata_aireas/data.json
mv ~/testdata_aireas/data.json ~/testdata_aireas/`grep -o -a -m 1 -h -r "date[^}]*" ~/testdata_aireas/data.json | head -1 | grep -o -E '[0-9]+'`.json

