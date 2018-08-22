#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from workflow import Workflow
from os import popen
from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')


def ip_ip(ip):
    ret = popen('curl ip.cn/' + ip).read()
    title = ret[ret.find('IP'):].replace('来自：', '  ').replace('：', ' : ')
    end = title.find('   ')
    wf.add_item(title=title, valid=True, arg=title[5:end])
    return title[5:end]


def ip_cip(ip):
    ret = popen('curl cip.cc/' + ip).read().split('\n')
    ip = ret[0].replace('\t', ' ')
    addr = ret[1][8:].replace(' ', '')
    operator = ret[2][12:]
    title = ip + '  ' + addr + '  ' + operator
    wf.add_item(title=title, valid=True, arg=ip[5:])
    return ip[5:]


def ipip(ip):
    def rep(str):
        return str.replace('[', '').replace('"', '').replace(']', '')

    ret = popen('curl freeapi.ipip.net/' + ip).read()
    ret = map(rep, ret.split(','))

    ip = 'IP : ' + ip
    addr = ret[0] + ret[1] + ret[2]
    operator = ret[4]
    title = ip + '  ' + addr + '  ' + operator
    wf.add_item(title=title, valid=True, arg=None)


def ip_ipip(ip1, ip2):
    ipip(ip1)
    if ip1 != ip2:
        sleep(1)
        ipip(ip2)


def main(wf):

    ip = sys.argv[1]

    ip1 = ip_ip(ip)

    ipip(ip1)

    ip2 = ip_cip(ip)

    if ip2 != ip1:
        sleep(1)
        ipip(ip2)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
