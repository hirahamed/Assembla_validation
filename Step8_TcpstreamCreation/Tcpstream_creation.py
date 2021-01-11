
import pyshark
from pprint import pprint
import json
import re
import os
import shutil


input_folder_path = "C:\\Users\\hira ahmed\\Desktop\\Signature Verification\\Drop4-Jan\\90\\"
wireshark_path = "C:\\Users\\hira ahmed\\Desktop\\wireshark"
output_tcp_folder_path = 'C:\\Users\\hira ahmed\\Desktop\\Signature Verification\\Drop4-Jan\\Created_TCPstreams_90Apps\\'
matched_json_file = "JAN_results_on_individualpcaps_90.json"
assembla_data_file = "assembla_data"


# Function to convert   
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1



def make_tcp_stream(wireshark_path, output_tcp_folder_path,gc_code,eq,activity_name,input_path, input_filename,itr):
	wireshark_path = wireshark_path
	tcp_folder_path = output_tcp_folder_path
	output_filename =  str(gc_code) +'_'+ str.upper(activity_name) +'_tcpstream-'+str(itr)+".pcap"

	if eq !=None:
		shutil.copy(input_path+"\\"+input_filename,wireshark_path)
		os.system(f'cmd /c "tshark -r {input_filename} -Y "tcp.stream eq "{eq} -w {output_filename}"')
		print("tcpstream created....!!")
		shutil.move(output_filename,tcp_folder_path)
		os.remove(input_filename)




def get_file_from_folder(folder, activity, index):
	for files_in_folder in folder:
		
		if ('.pcap' in files_in_folder) or ('.PCAP' in files_in_folder):
			file_name_split = files_in_folder.split('.')
			name_split = file_name_split[0].split('_')
			activity_name = ''
			activity_count = ''
			if '-' in name_split[1]:
					get_activity_name = list(map(lambda x: x.lower(),name_split[1].split('-')))
					if  get_activity_name[-2] == 'fail':
						sep = '-'
						activity_name = sep.join(get_activity_name[:-1])
						activity_count = get_activity_name[-1]
					else:
						if get_activity_name[-2] == 'only':
							sep = '-'
							activity_name = sep.join(get_activity_name[:-1])
							activity_count = listToString(get_activity_name[-1])

						else:
							activity_name = listToString(get_activity_name[:-1])
							activity_count = listToString(get_activity_name[-1])

			else:
				activity_name = name_split[1]
				activity_count = name_split[-1]
				
			if activity_count:
				activity_count = int(activity_count)

			if activity_name == str.lower(activity) and activity_count == int(index):
				return files_in_folder
				


with open(input_folder_path+assembla_data_file) as f:
  data = json.load(f)



files = os.listdir(input_folder_path)


# print(files)

with open(input_folder_path+matched_json_file) as f:
  matched_data = json.load(f)

counter = 0
for key, value in matched_data.items():


	app_name = key.replace(".","").replace(" ","").replace('-','').replace("'", '')
	app_name = app_name.lower()


	for f in files:

		f_split = f.split(' ')
		sep = ' '
		folder_name = sep.join(f_split[1:])

		if key == folder_name:
			folder = os.listdir(input_folder_path+f)

			activity_names_holder = []
			counter += 1
			print("Counter:		",counter, "........"," filename: ", f)
			inner_dict = {}
			gc_code = data[key]['Ticket_number']
			for activity in value:
		
				for val in value[activity]:
					# if activity == "LOGOUT":
					if type(val) == str:
						if ":" in val:
							splitted_Value = val.split(":")
							if splitted_Value[0] == 'tcp.stream eq':
								eq = int(splitted_Value[1].strip())
								app_folder =input_folder_path+f+'/' 
								pcapfilename = get_file_from_folder(folder,activity,0)
								make_tcp_stream(wireshark_path, output_tcp_folder_path ,gc_code,eq, activity,app_folder,pcapfilename,0)
								break
						else:
							print("Tcp cannot be created for : ",key," activity: ",activity)
				
					if type(val) == dict:
						for v in val:
							for d in val[v]:
								if ":" in d:
									splitted_Value = d.split(":")
									if splitted_Value[0] == 'tcp.stream eq':
										eq = int(splitted_Value[1].strip())
										app_folder =input_folder_path+f+'/' 
										pcapfilename = get_file_from_folder(folder,activity,v)
										make_tcp_stream(wireshark_path, output_tcp_folder_path,gc_code,eq, activity,app_folder,pcapfilename,v)
										break
								else:
									print("Tcp cannot be created for : ",key," activity: ",activity)
print("Done....")
