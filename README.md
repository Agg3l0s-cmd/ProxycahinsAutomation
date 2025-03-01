Script to get all free proxies from geonode.com and add the directly to proxycahins4.conf file. The script is made so that it gets only the elite anonymity proxeis that have a latency < 80ms.

I recomend to add it to crontab so the script updates the list whenever u want!

Run build.sh:
    chmod +x build.sh
    ./build.sh

Parameters: proxychains4.conf file location
--OPTIONAL--
If you want to use firefox use --firefox

How to run?
e.g. python main.py /etc/proxychains4.conf