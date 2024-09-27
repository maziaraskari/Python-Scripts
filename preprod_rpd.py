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
import access.thanos_preprod as access_thanos

thanos = ThanosQuery(access_thanos)
import access.genome_prod as genome_access

now = datetime.now()

array = []

# Remove all CSV files
for file in os.scandir("./preprdResults"):
    if file.name.endswith(".csv"):
        os.remove(file)


# Read a list of rpds from a text file 


df2 = pd.read_csv('preprod_rpd_in.txt', low_memory=False, sep=";")
p = len(df2)
print("number of input rpds are : ", p)
print("first rpd in list is", df2.iloc[0, 0])
print("last rpd in list is:", df2.iloc[p-1, 0])

thanos = ThanosQuery(access_thanos)
#print("thanos is ",thanos)
rpd= []




# add a pipe | to the elements in rpd array 

for i in range(0, p):
        rpd.append(df2.iloc[i, 0]+str('|'))
        
# convert all elements in array into one

string = ' '.join(rpd)
string = string.replace("| ", "|")
string = string[:-1]
print ("string is ",string)

#########################################################################################################################################################################
# Use Rich's thanos queries and get modems registration info 

query1 = "K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\"}"
print (query1)
thanos_info2 = thanos.instant(query=query1)
#print(thanos_info2)
cm_info = pd.DataFrame(thanos_info2[0])
cm_info = cm_info.set_index('ipv6Addr')
#cm_info = cm_info.set_index('cmMacAddr')

cm_info.to_csv("./preprdResults/PreProd_CmRegStatus_out.csv", mode='a',  header=(not os.path.exists('./preprdResults/PreProd_CmRegStatus_out.csv')))

#########################################################################################################################################################################
### open modem file above and get genome data

df3 = pd.read_csv('./preprdResults/PreProd_CmRegStatus_out.csv')
m3 = len(df3)
print ("Number of Modems we are getting data from Genome are :" , m3)
#print(df3.ipv6Addr)
ips = [ip for ip in df3.ipv6Addr if ip.count('0') < 32]
genome = BasicQueries(genome_access)
#genome_info = genome.cm_params(ips, fields='all').set_index('mac')
genome_info = genome.cm_params(ips, fields='all').set_index('ip')
genome_info.to_csv('./preprdResults/PreProd_genomeInfo.csv', mode='a',  header=not os.path.exists('./preprdResults/PreProd_genomeInfo.csv'))

#########################################################################################################################################################################

#Mazi = df3.join(genome_info, how='outer', rsuffix='_g' )
Mazi = cm_info.join(genome_info, how='outer', lsuffix='_g' ) ### notice the joined files are not dataframe..
#Mazi = pd.merge(genome_info, df3,  on=["ipv6Addr","ip"], how="inner")
Mazi.to_csv("./preprdResults/PreProd_CmRegStatusPlusGenome_out.csv", mode='a', header=(not os.path.exists('./preprdResults/PreProd_CmRegStatusPlusGenome_out.csv')))

#########################################################################################################################################################################

query2 = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"d30_online\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual)"
print (query2)
thanos_info2 = thanos.instant(query=query2)
#print(f"Tanos info  0 is \n, {thanos_info2[0]}")
#print(f"Tanos info 1 is \n, {thanos_info2[1]}")
cm_info2 = pd.DataFrame(thanos_info2[0])
cm_info3 = pd.DataFrame(thanos_info2[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./preprdResults/PreProd_d30_online.csv", mode='a', header=(not os.path.exists('./preprdResults/PreProd_d30_online.csv')))

#########################################################################################################################################################################

query = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"d31_online\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual) "
print (query)
thanos_info = thanos.instant(query=query)
#print(f"Tanos info  0 is \n, {thanos_info[0]}")
#print(f"Tanos info 1 is \n, {thanos_info[1]}")
cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./preprdResults/PreProd_d31_online.csv", mode='a', header=(not os.path.exists('./preprdResults/PreProd_d31_online.csv')))
#########################################################################################################################################################################

query = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"p_online\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual) "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./preprdResults/PreProd_p_online.csv", mode='a', header=(not os.path.exists('./preprdResults/PreProd_p_online.csv')))
#########################################################################################################################################################################

query = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"dhcpv6Complete\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual) "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./preprdResults/PreProd_dhcpv6Complete.csv", mode='a', header=(not os.path.exists('./preprdResults/PreProd_dhcpv6Complete.csv')))

#########################################################################################################################################################################

query = "count(K_CmRegStatus_RegStatus{rpdName=~\"" + string + "\", regStatus=\"offline\"}) by (rpdName,regStatus,cmMacAddr,ofdmActual) "
print (query)
thanos_info = thanos.instant(query=query)

cm_info2 = pd.DataFrame(thanos_info[0])
cm_info3 = pd.DataFrame(thanos_info[1])
cm_info4 = cm_info2.join(cm_info3)
cm_info4.to_csv("./preprdResults/PreProd_offline.csv", mode='a', header=(not os.path.exists('./preprdResults/PreProd_offline.csv')))
# read_file = pd.read_csv ('CmRegStatusGenome.csv')
# read_file.to_excel ('CmRegStatusGenome.xlsx', index = None, header=True)


#########################################################################################################################################################################





print("Finished")
