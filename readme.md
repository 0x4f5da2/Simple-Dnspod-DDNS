# Simple Dnspod DDNS

## Prerequisites

* requests

# Installation

* `python3 setup.py install`

* add token to ddns.py

* set crontab, e.g., `*/30 * * * * /usr/bin/python3 /home/pi/cron/ddns/ddns.py >> /home/pi/ddns.log`