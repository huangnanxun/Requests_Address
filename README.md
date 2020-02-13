## Requests_Address
## Nanxun Huang, CSCI4211, 02/13/2020

### setup code instruction:
  1. copy Requests_Address.py and DNSClientV3.py to folder

### Execution/Running section
  1. Run python Requests_Address.py
  2. In Requests_Address.py, follow instruction to select dnsSelection_mode
  3. After showing "Server is listening..." , Run python DNSClientV3.py
  4. Query on DNSClientV3

### Description section
  This program use port 9889, listen to queries from DNSClientV3, use gethostbyname_ex to get host information,
  store the information into cache in dict form (json) in DNS_mapping.txt, send message back as well as save
  log in dns-server-log.csv
