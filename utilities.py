#!usr/bin/python2.7
# -*- coding=utf-8 -*-
#import requests
import pexpect
import re
from dns import resolver

Highest_Latency = 99999.99


#检查ping的返回速度
def check_ping_time(ip):
    if if_ip_address(ip):
        (command_output, exitstatus) = pexpect.run("ping -c1 %s" % ip, timeout=5, withexitstatus=1)
        if exitstatus == 0:
            #print command_output
            m = re.search("time=([\d\.]+)", command_output)
            if m:
                #print 'time=', m.group(1)
                return float(m.group(1))
        else:
            return Highest_Latency #set a large number to mark down the server. 
    else:
        return Highest_Latency

#将域名解析为IP地址
def url_to_ip(url):
    #address = []
    res = resolver.Resolver()
    res.nameservers = ['8.8.8.8','192.168.1.1']
    try:
        answers = res.query(url, 'A')
        return answers[0].address #always use the first answer if multiple records configured. 
    except:
        return False

#检查是否是IP
def if_ip_address(one_str):  
    ''''' 
    正则匹配方法 
    判断一个字符串是否是合法IP地址 
    '''  
    compile_ip=re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')    
    if compile_ip.match(one_str):    
        return True    
    else:    
        return False  

#从快到慢排序
def server_sort(list):
    return list

#写入新的config文件
def update_config_file(config):
    nginx_conf_temp = '''stream {{
        {upstream_groups}
        {servers}
}} 
'''
    upstream_groups = ""
    servers = ""

    upstream_temp = '''
        upstream {group_name} {{
            hash $remote_addr consistent;
            {server_list}
        }}
    '''

    server_list_temp = '''server {ip_address}:{port} weight={weight};
            '''

    server_temp = '''
        server {{
            listen {port};
            listen {port} udp;
            proxy_pass {group_name};
        }}
    '''
    server_port = 443
    for key in config.keys():
        server_list = ""
        server_weight = 50
        for server in config[key]:
            server_list += server_list_temp.format(ip_address=server[0],port=server[1],weight=server_weight)
            server_weight -= 1
        upstream_groups += upstream_temp.format(group_name=key,server_list=server_list)
        servers += server_temp.format(port=server_port,group_name=key)
        server_port += 1

    nginx_conf = nginx_conf_temp.format(upstream_groups=upstream_groups, servers=servers)
    handle = open('/etc/nginx/sites-enabled/ssrproxy','w')
    #handle = open('./ssrproxy','w')
    handle.write(nginx_conf)
    handle.close()  
    return 0

