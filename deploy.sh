cd /var/www/vhosts/jasper.meteostat.net/meteostat-server
git fetch --all && git reset --hard origin/master
sh ./tasks/db_import.sh
python3 -m pip install . -U
cat crontab > /var/spool/cron/crontabs/jasper
/etc/init.d/apache2 restart
