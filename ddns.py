#!/usr/bin/env python
# -*- coding:utf-8 -*-


from dnspod import apicn
import json
import requests
import re
import time

def get_ip():
    # getting current IP 
    resp = requests.get("https://www.ip.cn/api/index?ip=&type=0")
    content = resp.content.decode('utf-8')
    obj = json.loads(content)
    ip_addr = obj["ip"]
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip_addr):
        return ip_addr
    else:
        return None


def main():
    print(time.ctime())
    login_token = "123456,0123456789abcdef0123456789abcdef"  # replace with your own token
    target_subdomain = "test"  # replace with your subdomain
    target_domin = "example.com"  # replace with your domain
    cur_local_ip = get_ip()
    assert cur_local_ip is not None

    print("DomainList")
    api = apicn.DomainList(login_token=login_token)
    domain_ids = api().get("domains")
    print(domain_ids)
    target_domain_id = None
    for d in domain_ids:
        if d['name'] == target_domin:
            target_domain_id = d['id']
            break
    assert target_domain_id is not None

    print("RecordList")
    api = apicn.RecordList(target_domain_id, login_token=login_token)
    records = api().get("records")
    target_record_id = None
    cur_dns_record_ip = None
    for r in records:
        if r['name'] == target_subdomain:
            target_record_id = r['id']
            cur_dns_record_ip = r['value']
    print(records)
    assert target_record_id is not None
    if cur_dns_record_ip != cur_local_ip:
        print("RecordModify", target_record_id)
        api = apicn.RecordModify(target_record_id, sub_domain=target_subdomain, record_type="A", record_line='默认'.encode("utf8"), value=cur_local_ip, ttl=600, domain_id=target_domain_id, login_token=login_token)
        print(api())
    else:
        print("Skip!")


if __name__ == '__main__':
    main()
