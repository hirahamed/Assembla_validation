
import os
import scapy
from scapy.layers.inet import IP
from scapy.all import *
from pprint import pprint
from scapy.layers import http
import pprint
import json
import re
import shutil
from pprint import pprint



count=1

def merge_pcap(path, file_name,pkt):
	string = '_master.pcap'
	pcap_name = file_name + string
	wrpcap(pcap_name, pkt, append=True)  #appends packet to output file
	

def move_master_pcaps(filename, source, dest):
	shutil.move(source + filename, dest)

def open_pcap_from_local(file_name):
	pcap_file_name=file_name
	fil= open(pcap_file_name,'rb')
	a=rdpcap(fil)
	return a 


# def remove_file_from_local(filename):
# 	os.remove(filename)


fileID={}
file_content={ }

assembla_data = {}

# load assembla_data.json
with open('assembla_data') as f:
  data = json.load(f)






arr = os.listdir()
files = []
# print(arr)
for f in arr:
	# print(f)
	if '.' in f:
		ex = f.split(".")
		if ex[1] == 'pcap' or ex[1] == 'PCAP':
			files.append(f)


dest = 'C:\\Users\\hira ahmed\\Desktop\\Signature Verification\\Drop4-Jan\\MasterPcapsfor_100Apps\\'
for file_name in arr:
	hold = file_name.split(" ")
	if hold[0].isdigit():
		inside_files = os.listdir(os.getcwd()+'/'+file_name)
		print(inside_files)
		for app in inside_files:
			a = app.split('.')
			if a[-1] == 'pcap' or a[-1] == 'PCAP':
				print(app)
				pcap_data = open_pcap_from_local(os.getcwd()+'/'+file_name+"/"+app)
				merge_pcap(os.getcwd()+'/'+file_name+"/", hold[0],pcap_data)
		move_master_pcaps(hold[0]+"_master.pcap",os.getcwd()+'/',dest)
