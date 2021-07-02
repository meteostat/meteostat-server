CONFIG_PATH='/var/www/.meteostat-server/config.ini'

DB_USER=`sed -nr "/^\[database\]/ { :l /^user[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $CONFIG_PATH`
DB_PASS=`sed -nr "/^\[database\]/ { :l /^password[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $CONFIG_PATH`
DB_NAME=`sed -nr "/^\[database\]/ { :l /^name[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $CONFIG_PATH`

curl 'https://bulk.meteostat.net/v2/internal/stations.sql' | mysql -u $DB_USER -p$DB_PASS $DB_NAME
curl 'https://bulk.meteostat.net/v2/internal/inventory.sql' | mysql -u $DB_USER -p$DB_PASS $DB_NAME
