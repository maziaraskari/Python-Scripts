#!/usr/bin/env python3

import pandas as pd
import csv
import os
import webbrowser
import numpy as np
from csv import writer
from datetime import datetime

from hfc_tools.thanos import ThanosQuery, query_builder
from hfc_tools.genome import BasicQueries

import access.thanos_prod as access_thanos
import access.genome_prod as genome_access

thanos = ThanosQuery(access_thanos)

now = datetime.now()

array = []

# Remove all CSV files
for file in os.scandir("./results"):
    if file.name.endswith(".csv"):
        os.remove(file)


# Read a list of rpds from a text file 


df2 = pd.read_csv('prod_rpd_in.txt', low_memory=False, sep=";")
p = len(df2)
print("number of input rpds are : ", p)
print("first rpd in list is", df2.iloc[0, 0])
print("last rpd in list is:", df2.iloc[p-1, 0])



rpd= []



# add a pipe | to the elements in rpd array 
for i in range(0, p):
        rpd.append(df2.iloc[i, 0]+str('|'))
        
# convert all elements in array into one
string = ' '.join(rpd)
string = string.replace("| ", "|")
string = string[:-1]
print ("string is ",string)


# Use Rich's thanos queries and get modems registration info 
query1 = "K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\"}"
print (query1)
thanos_info2 = thanos.instant(query=query1)
#print(thanos_info2)
cm_info = pd.DataFrame(thanos_info2[0])
cm_info = cm_info.set_index('ipv6Addr')
cm_info.to_csv("./results/PROD_CmRegStatus_out.csv", mode='a', header=(not os.path.exists('./results/PROD_CmRegStatus_out.csv')))

##########################################################################################################################################
### open modem file above and get genome data

df3 = pd.read_csv('./results/PROD_CmRegStatus_out.csv')
m3 = len(df3)
print ("Number of Modems we are getting data from Genome are :" , m3)
print(df3.ipv6Addr)
ips = [ip for ip in df3.ipv6Addr if ip.count('0') < 32]

#print(ips)
genome = BasicQueries(genome_access)

genome_info = genome.cm_params(ips, fields='all').set_index('ip')
genome_info.to_csv('./results/GenomeInfo_From_Modem_IPv6.csv', mode='a', index=True, header=not os.path.exists('./results/GenomeInfo_From_Modem_IPv6.csv'))
#Mazi = df3.join(genome_info, how='outer', rsuffix='_g')
Mazi = cm_info.join(genome_info, how='outer', rsuffix='_g')
Mazi.to_csv("./results/PROD_CmRegStatusPlusGenome_out.csv", mode='a', header=(not os.path.exists('./results/PROD_CmRegStatusPlusGenome_out.csv')))

##########################################################################################################################################
# Find D3.0 Modems
query2 = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"d30_online\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual) "
print (query2)
query2a = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"d30_online\"})"
print (query2a)
thanos_info2 = thanos.instant(query=query2)
cm_info2 = pd.DataFrame(thanos_info2[0])
cm_info3 = pd.DataFrame(thanos_info2[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./results/PROD_d30_online.csv", mode='a', header=(not os.path.exists('./results/PROD_d30_online.csv')))


query = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"d31_online\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual) "
print (query)
thanos_info = thanos.instant(query=query)
#print(f"Tanos info  0 is \n, {thanos_info[0]}")
#print(f"Tanos info 1 is \n, {thanos_info[1]}")
cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./results/PROD_d31_online.csv", mode='a', header=(not os.path.exists('./results/PROD_d31_online.csv')))

query = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"p_online\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual) "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./results/PROD_p_online.csv", mode='a', header=(not os.path.exists('./results/PROD_p_online.csv')))

query = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"dhcpv6Complete\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual) "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./results/PROD_dhcpv6Complete.csv", mode='a', header=(not os.path.exists('./results/PROD_dhcpv6Complete.csv')))


query = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"offline\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual) "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./results/PROD_offline.csv", mode='a', header=(not os.path.exists('./results/PROD_offline.csv')))




query = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\"}) by (regStatus) "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./results/PROD_regStatus.csv", mode='a', header=(not os.path.exists('./results/PROD_regStatus.csv')))



query = "instance:snmp_docsIfSigQExtUncorrectables_snmp_docsIfSigQExtCorrecteds_snmp_docsIfSigQExtUnerroreds:sumdiv{rpdName=~\"" + string + "\",ifName=~\"Us+.*\"} > 0.01 "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./results/PROD_instantaneus_US_SCQAM_UNCORRECTED_FEC_>0.01prcnt.csv", mode='a', header=(not os.path.exists('./results/PROD_instantaneus_US_SCQAM_UNCORRECTED_FEC_>0.01prcnt.csv')))


query = "avg(snmp_docsIfSigQSignalNoise{rpdName=~\"" + string + "\", ifName=~\"Us+.*\"}) by (rpdName) "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./results/PROD_AVG_USSCQAM_SNR.csv", mode='a', header=(not os.path.exists('./results/PROD_AVG_USSCQAM_SNR.csv')))



query = "avg(K_CmUsPerf_RxPower{rpdName=~\"" + string + "\", ifName=~\"Us+.*\"}) by (rpdName) "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./results/PROD_AVG_USSCQAM_RxPower.csv", mode='a', header=(not os.path.exists('./results/PROD_AVG_USSCQAM_RxPower.csv')))







# read_file = pd.read_csv ('CmRegStatusGenome.csv')
# read_file.to_excel ('CmRegStatusGenome.xlsx', index = None, header=True)

print("Finished")
