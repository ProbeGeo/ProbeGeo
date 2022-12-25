a = 0
while [ $a -lt 55000];
do
    python crawl_ip_geo.py --start $a
    a=$(($a+500))
done