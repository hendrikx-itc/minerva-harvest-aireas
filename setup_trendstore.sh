for i in /data/trendstore/*.json
do
    PGDATABASE=minerva PGHOST=database PGUSER=postgres /usr/local/bin/minerva trend-store create --from-json $i
done
touch /tmp/trendstoredone
