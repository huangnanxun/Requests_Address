#!/usr/bin/env python
# coding: utf-8

# ## Request address to IP translation (DNS)

# ### Programming Project 1  - Nanxun Huang

# In[1]:


import sys, threading, os, random
from socket import *


# In[2]:


import pandas as pd
import numpy as np
import json


# In[3]:


def get_dnsSelection_mode():
    print("Choose whether to choose ip according to ping value the DnsSelection code          \nY for Yes and N for No\nNotice:If you choose Y please make sure package pythonping has installed")
    get_valid_input = False
    while(1):
        dnsSelection_mode = input()
        if (dnsSelection_mode == 'Y' or dnsSelection_mode == 'y'):
            return True
        if (dnsSelection_mode == 'N' or dnsSelection_mode == 'n'):
            return False
        else:
            print("Wrong input, Plase enter again.")


# In[4]:


def dnsSelection_mode_n(ipList):
    if len(ipList) == 0:
        return('Empty ip list')
    else:
        return(ipList[0])


# In[5]:


def dnsSelection_mode_y(ipList):
    from pythonping import ping
    if len(ipList) == 0:
        return('Empty ip list')
    else:
        ping_delay_list = list(map(lambda x: ping(x, size=4, count=1).rtt_avg_ms, ipList))
        min_index = ping_delay_list.index(min(ping_delay_list))
        return(ipList[min_index])


# In[6]:


def read_cache_to_dict():
    f = open('DNS_mapping.txt','r')
    if not(f.read()):
        my_dict = dict()
    else:
        with open('DNS_mapping.txt', 'r') as f:
            my_dict = json.load(f)
    return my_dict


# In[7]:


def write_dict_to_cache(my_dict):
    f = open('DNS_mapping.txt','w')
    json.dump(my_dict,f)


# In[8]:


def dnsQuery(connectionSock, srcAddress):
    c_input = connectionSock.recv(1024)
    DNS_mapping_dict = read_cache_to_dict()
    host_exist = True
    try:
        input_host_info = gethostbyname_ex(c_input)
        input_hostname = input_host_info[0]
        input_ip = input_host_info[2]
    except:
        input_hostname = 'Host not found'
        input_ip = 'Host not found'
        host_exist = False
    if (host_exist):
        if (input_hostname in DNS_mapping_dict.keys()):
            ip_list = DNS_mapping_dict[input_hostname]
        else:
            ip_list = input_ip
            DNS_mapping_dict[input_hostname] = ip_list
            write_dict_to_cache(DNS_mapping_dict)
        
        if (get_dnsSelection_mode):
            ip_addr = dnsSelection_mode_y(ip_list)
        else:
            ip_addr = dnsSelection_mode_n(ip_list)
    else:
        ip_addr = input_ip
    write_dict_to_cache(DNS_mapping_dict)
    message = c_input.decode()+":<"+input_hostname+">:<"+ip_addr +">"
    message = str.encode(message) 
    connectionSock.send(message)
    dns_server_log = open('dns-server-log.csv','a')
    dns_server_log.write('\n'+c_input.decode()+','+ip_addr)
    dns_server_log.close()


# In[9]:


def monitorQuit():
    while 1:
        sentence = input()
        if sentence == "exit":
            os.kill(os.getpid(),9)


# In[10]:


import sys, threading, os, random
from socket import *

def main():
    host = "localhost" 
    port = 9889
    get_dnsSelection_mode()
    sSock=socket(AF_INET,SOCK_STREAM)
    sSock.bind((host,port))
    sSock.listen(20)  
    monitor = threading.Thread(target=monitorQuit, args=[])
    monitor.start()
    print("Server is listening...")
    while 1:
        connectionSock, addr = sSock.accept()
        server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
        server.start()


# In[11]:


main()





