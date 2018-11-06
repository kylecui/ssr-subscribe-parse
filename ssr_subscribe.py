#!/usr/bin/python
# -*- coding=utf-8 -*-
import sys
from collections import OrderedDict
#import subprocess
from Queue import Queue
from threading import Thread

import utilities
#try:
#no python3
from ssrParse2 import ssrParse

#except:
#    from ssrParse3 import ssrParse


def retrieve_subscribe(url):
    #no python3
    #pythonVersion = int(sys.version_info.major)
    ssrList = ssrParse.parseSubscribe(url)
    info = ssrParse()
    for item in ssrList:
        if len(item) > 0:
            info.decode(item)
            dict = info.format()
            server = dict['server'].decode("utf-8")
            if not utilities.if_ip_address(server):
                dict['server'] = utilities.url_to_ip(server)
            queue.put(dict)
            #dict['speed'] = utilities.check_ping_time(ip)
            # for key in dict.keys():
            #     #if pythonVersion == 2:
            #     # no python3
            #     print(":".join([key, str(dict[key]).decode("utf-8")]))
            #     #elif pythonVersion == 3:
            #     #    print(":".join([key, str(dict[key])]))
            # print ("\n")

#thread worker
def ping_worker(i,q):
    while True:
        dict = q.get()
        dict['speed'] = utilities.check_ping_time(dict['server'])
        #for key in dict.keys():
            #print(":".join([key, str(dict[key]).decode("utf-8")]))
        #print ("\n")
        
        if dict['speed'] < utilities.Highest_Latency: #otherwise, drop the dead server
            server_alive = (dict['server'],
                            dict['server_port'],
                            dict['speed'],
                            dict['remarks']
            )
            ActiveServers.append(server_alive)
        
        q.task_done()

queue = Queue()
ActiveServers = []
if __name__ == '__main__':
    if len(sys.argv) == 2:
        retrieve_subscribe(sys.argv[1])
    else:
        retrieve_subscribe('https://panel.myharbour.website//s/hNesN')
    
    #多线程ping服务器，获得时间反馈
    num_threads = 5
    for i in range(num_threads):
        worker = Thread(target=ping_worker,args=(i,queue))
        worker.setDaemon(True)
        worker.start()
    
    #print "-- iPaddress  | State -- "
    queue.join()
    #print "------ End ---------"

    def get_third(elem):
        return elem[2]
    
    ActiveServers.sort(key=get_third)
    HKServers=[]
    USServers=[]
    SGServers=[]
    TWServers=[]
    JPServers=[]
    DEServers=[]
    AllOthers=[]

    #print("{}\t{}\t{}\t{}".format("server","port","latency","remark"))
    for server in ActiveServers:
        #print("{}\t{}\t{}\t{}".format(server[0],server[1],server[2],server[3]))
        if server[3].startswith('LA'):
            USServers.append(server)
        elif server[3].startswith('HKT'):
            HKServers.append(server)
        elif server[3].startswith('SG'):
            SGServers.append(server)
        elif server[3].startswith('TW'):
            TWServers.append(server)
        elif server[3].startswith('JP'):
            JPServers.append(server)
        elif server[3].startswith('DE'):
            DEServers.append(server)
        else:
            AllOthers.append(server)
    
    config_dict = OrderedDict()
    config_dict['US'] = USServers
    config_dict['HK'] = HKServers
    config_dict['SG'] = SGServers
    config_dict['TW'] = TWServers
    config_dict['JP'] = JPServers
    config_dict['DE'] = USServers
    config_dict['Other'] = AllOthers
    
    utilities.update_config_file(config_dict)
    print("{}\t{}\t{}\t{}".format("server","port","latency","remark"))
    for server in HKServers:
        print("{}\t{}\t{}\t{}".format(server[0],server[1],server[2],server[3]))    
    print('\n')
    print("{}\t{}\t{}\t{}".format("server","port","latency","remark"))
    for server in USServers:
        print("{}\t{}\t{}\t{}".format(server[0],server[1],server[2],server[3]))    
    print('\n')
    print("{}\t{}\t{}\t{}".format("server","port","latency","remark"))
    for server in SGServers:
        print("{}\t{}\t{}\t{}".format(server[0],server[1],server[2],server[3]))    
    print('\n')
    print("{}\t{}\t{}\t{}".format("server","port","latency","remark"))
    for server in TWServers:
        print("{}\t{}\t{}\t{}".format(server[0],server[1],server[2],server[3]))    
    print('\n')
    print("{}\t{}\t{}\t{}".format("server","port","latency","remark"))
    for server in JPServers:
        print("{}\t{}\t{}\t{}".format(server[0],server[1],server[2],server[3]))    
    print('\n')
    print("{}\t{}\t{}\t{}".format("server","port","latency","remark"))
    for server in DEServers:
        print("{}\t{}\t{}\t{}".format(server[0],server[1],server[2],server[3]))    
    print('\n')
    print("{}\t{}\t{}\t{}".format("server","port","latency","remark"))
    for server in AllOthers:
        print("{}\t{}\t{}\t{}".format(server[0],server[1],server[2],server[3]))    
