import pyshark
from pprint import pprint
import json
import re
import os




def open_pcap_packets(pcap_file, filename):

	sess_index = [] # to save stream indexes in an array
	for pkt in pcap_file:
		try:
			sess_index.append(pkt.tcp.stream)
		except:
			pass

	stream_indexes = sorted(set(sess_index))
	pcap_file.close()
	pcap_file = filename

	packets_dict = {}
	for i in stream_indexes:
		# print('\n')
		print('TCP stream number :',str(int(i)))
		req_header_flag = 1
		req_payload_flag = 0
		resp_header_flag = 0 
		resp_payload_flag = 0
		# # print(int(i))
		# if int(i) != 0:
		# 	continue
		capture = pyshark.FileCapture(pcap_file, display_filter='tcp.stream eq %d' % int(i))
		packet_lst = {}
		request_header_lst = []
		request_payload_lst = []
		response_header_lst = []
		response_payload_lst= []
		for packet in capture:


			field_names = packet.tcp._all_fields
			if 'tcp.payload' in field_names.keys():
				str_test = field_names['tcp.payload'].split(':')
				str_test2 = ''.join(str_test)
				pack = bytearray.fromhex(str_test2).decode("utf-8")
				lines = pack.split('\n')

				for l in lines:
		
					if not l and req_header_flag == 1:
						req_header_flag = 0
						req_payload_flag =1
						# print('\n')

					if req_header_flag == 1:
						if not l:
							continue
						# print(l)
						request_header_lst.append(l)
						#print('request header : ', l)

					if req_payload_flag == 1 and not l.startswith('HTTP/1.'):
						if not l:
							continue

						# if 'ACK' not in l:
						# 	if ('Continuation' not in l) :
						request_payload_lst.append(l)
								# print('request payload : ', l)
						
					if req_payload_flag == 1 and l.startswith('HTTP/1.'):
						req_payload_flag =0 
						resp_header_flag = 1
						# print('\n')


					if not l and resp_header_flag == 1:
						resp_header_flag= 0
						resp_payload_flag =1
						# print('\n')

					if resp_header_flag == 1:
						if not l:
							continue
						response_header_lst.append(" "+l)
						# print('response header : ', l)


					if resp_payload_flag ==1:
						if not l:
							continue
						response_payload_lst.append(l)
						# print('response payload : ',l)

				packet_lst['request header'] = request_header_lst
				packet_lst['request payload'] = request_payload_lst
				packet_lst['response header'] = response_header_lst
				packet_lst['response payload'] = response_payload_lst

						

			packets_dict['tcp.stream eq %d' % int(i)] = packet_lst


		capture.close()

	return packets_dict


def replace_special_characters(str1):
	# print(str1)
	# str1 = '"client_req_id":*'
	# print(str1)
	lst = []
	if ',' in str1:
		lst1 = str1.split(',')

		
		# print(lst)
		# print(lst[0])
		# print(lst[1])
		for l in lst1:
			# print("^^^^^^^^^^^^^^^")
			# print(l)
			hold = ''
			last_element = lst1[-1]
			# print("**************")
			# print(l)
			# print("**************")
			if l.endswith(':') or l.endswith('='):
				if last_element != l:
					# print("___________")
					hold = l+".*,"
				else:
					hold = l+".*"

			if '+' in l:
				# print("----------")
				# print(l)
				hold = l.replace('+', r'.+')
				# print(hold)
			elif r'\+' in l:
				hold = l
				
			if '[' in l:
				hold = l.replace("[",r".*")

			if ']' in l:
				hold = l.replace("]",r".*")

		

			if '(' in l:
				hold = l.replace("(",r"\(")

			if ')' in l:
				hold = l.replace(")",r"\)")

			if '$' in l:
				hold = l.replace("$",r"\$")

			if '{' in l:
				hold = l.replace("{",r"\{")

			if '}' in l:
				hold = l.replace("}",r"\}")

			if "'" in l:
				hold = l.replace("'",r"'")

			# if '_' in l:
			# 	hold = l.replace("_",r"\_")


			if '\\' in l:
				hold = l.replace("\\",r".*")
			

			# if l.endswith("*"):
			# 	hold = l.replace("*",".*,")

			if '?' in l:
				# print("----------")
				# print(l)
				hold = l.replace('?', r'\?')
				# print(hold)
			elif r'\?' in l:
				hold = l

			# if ':' in l:
			# 	# print("----------")
			# 	# print(l)
			# 	hold += l.replace(':', r'\:')
			# 	# print(hold)
			# elif r'\:' in l:
			# 	hold += l

			if '.*' in l:
				hold = l
			elif '*' in l:
		
				hold = l.replace('*','.*')
			
		
			if '-' in l:
				hold = l.replace('-',r'\-')
			
			if last_element != l:
				# print("====!!!!!")
				# print(l)
				if hold:

					hold = hold + ","
				else:
					hold = l +","
				
				lst.append(hold)
			else:
				# print(l)
				if hold:
					hold = hold
				else:
					hold = l
				
	
				lst.append(hold)
		# print(lst)
		
	
	else:
		

		# print(l)
		if str1.endswith(":") or str1.endswith('='):
			str1 =str1+".*"



		if '.*' in str1:
			str1 = str1
		elif '*' in str1:
			
			str1 = str1.replace('*','.*')


		if "'" in str1:
			str1 = str1.replace("'",r"\'")
	
		if '[' in str1:
			str1 = str1.replace("[",r".*")

		if ']' in str1:
			str1 = str1.replace("]",r".*")

		if '(' in str1:
			str1 = str1.replace("(",r"\(")

		if ')' in str1:
			str1 = str1.replace(")",r"\)")

		if '{' in str1:
			str1 = str1.replace("{",r"\{")

		if '}' in str1:
			str1 = str1.replace(")",r"\}")

		if '$' in str1:
			str1 = str1.replace("$",r"\$")

		if '\\' in str1:
			str1 = str1.replace("\\",r".*")

		if "+" in str1:
			str1 = str1.replace("+",".+")
		elif r"\+" in str1:
			str1 = str1


		if '-' in str1:
			str1 = str1.replace('-',r'\-')

		if '?' in str1:
			# print("----------")
			# print(l)
			str1 = str1.replace('?', r'\?')
			# print(hold)
		elif r'\?' in str1:
			str1 = str1


		lst.append(str1)
		# print(lst)
	str12 =""
	# print("----------------")
	# print(lst)
	return str12.join(lst)

def multiple_values(req_method, req_method2):
	ls = []
	if req_method and req_method2:
		# print("************")
		# print(req_method)
		# print(req_method2)
		ls.append(req_method)
		if '|' in req_method2:
			x = req_method2.split('|')
			for p in x:
				ls.append(p)
		else:
			ls.append(req_method2)
		
	else:
		ls.append(req_method)
	# print(ls)
	return len(ls), ls

def separate_values(value):
	lst = []
	if '|' in value:
		hold = value.split('|')
		for h in hold:
			lst.append(h)
	else:
		lst = value
	
	return lst


# Function to convert   
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1

def pattern_matching(packets_dict, value, activity, app_name):
	found_flag_list = []
	final_results = []

	req_method = ''
	req_host = ''
	req_uri = ''
	req_params = ''
	req_header = ''
	req_payload = ''
	resp_code = ''
	resp_header = ''
	resp_payload = ''
	req_method = replace_special_characters(value["custom_fields"][activity+"_req-method"].strip())
	if req_method:
		# print(req_method)
		req_method = re.compile(str(req_method))

	req_host = replace_special_characters(value["custom_fields"][activity+"_req-host"].strip())

	if req_host:
		
		req_uri = replace_special_characters(value["custom_fields"][activity+"_req-uri-path"].strip())
		# print(req_uri)
		if req_uri:
			host_and_uri = req_host + req_uri
			req_host = re.compile(host_and_uri)
			# print("========")
			# print(req_host)
			
		else:
			req_host = re.compile(req_host)
	
		print(req_host)
	# req_uri = replace_special_characters(value["custom_fields"][activity+"_req-uri-path"].strip())
	# if req_uri:
	# 	# print(req_uri)
	# 	req_uri = re.compile(req_uri)

	req_params = replace_special_characters(value["custom_fields"][activity+"_req-params"].strip())
	# if req_params:
	# 	req_params = re.compile(req_params)

	req_header = replace_special_characters(value["custom_fields"][activity+"_req-headers"].strip())
	# if req_header:
	# 	req_header = re.compile(req_header)

	# print("**********____________________")
	# print(value["custom_fields"][activity+"_req-payload"])
	req_payload = replace_special_characters(value["custom_fields"][activity+"_req-payload"].strip())
	# print("**********____________________")
	# print(req_payload)
	# if req_payload:

	# 	req_payload = re.compile(req_payload)

	if activity == 'LOGIN' or activity == 'LOGIN-FAIL':
		
		resp_code = replace_special_characters(value["custom_fields"][activity+"_resp-code"].strip())
		if resp_code:
			resp_code = re.compile(resp_code)

		resp_header = replace_special_characters(value["custom_fields"][activity+"_resp-header"])


		resp_payload = replace_special_characters(value["custom_fields"][activity+"_resp-payload"].strip())
		# print("8888888888")
		# print(resp_payload)




	for eq, packet in packets_dict.items():

		matched_result = []					
		
		flag = False
		

		converted_reqHead_str = listToString(packet['request header'])
		# print(converted_reqHead_str)
		for element in packet['request header']:
		
			question_mark_break = ''
			splitted_element = element.split(' ')
			
			if req_method:
				# if req_method.match(str(splitted_element[0])):
					# print(element)
				# print("METHOD --------- ")
				# print(req_method)
				# print(splitted_element[0])
				# print(splitted_element[1])
			
				# if req_uri:
				# 	if  req_method.match(str(splitted_element[0])) and req_host.search(str(splitted_element[1])) and req_uri.search(str(splitted_element[1])):
				# 		matched_result.append("Matched_Req_Method: "+str(splitted_element[0]))
				# 		matched_result.append("Matched_Host: "+str(splitted_element[1]))	
				# 		matched_result.append("Matched_Uri: "+str(splitted_element[1]))	
				# 		flag = True
				# 	else:
				# 		flag = False

				# else:		
				if req_host:	
					# print("----------")
					# if '?' in splitted_element[1]:
					# 	question_mark_break =  splitted_element[1].split("?")
					# 	print(question_mark_break)
					# print(req_host)
					# print(splitted_element[1])
					if req_method.match(str(splitted_element[0])) and req_host.search(str(splitted_element[1])):
						question_mark_break = splitted_element[1].split("?")
						# print("YES")
	
						if req_host.search(question_mark_break[0]):
							matched_result.append("Matched_Req_Method: "+str(splitted_element[0]))
							matched_result.append("Matched_Host: "+str(splitted_element[1]))
							matched_result.append("Matched_Uri: "+str(splitted_element[1]))
							flag = True
						else:
							flag = False

					if flag == True:
						break

		if flag == True:
			if req_params: 
				break_params = ''
				if ',' in req_params:
					req_params_splitted = req_params.split(",")
					
					for req_parm1 in req_params_splitted:
						req_params_re = re.compile(req_parm1)
						converted_reqParam_str = listToString(packet['request header'])
						if "?" in converted_reqParam_str:
							break_params = converted_reqParam_str.split("?")
							break_on_space = break_params[1].split(" ")
							if req_params_re.search(str(break_on_space[0])):
								# inner_dict['Matched_Params'] = element
								matched_result.append("Matched_Params: "+str(break_on_space[0]))
								flag = True
							else:
								flag = False
						else:
							flag = False
				else:
					req_params_original = re.compile(req_params)
					converted_reqParam_str = listToString(packet['request header'])
					
					
					if "?" in converted_reqParam_str:
						break_params = converted_reqParam_str.split("?")
						break_on_space = break_params[1].split(" ")
						if req_params_original.search(str(break_on_space[0])):
						
							# inner_dict['Matched_Params'] = element
							matched_result.append("Matched_Params: "+str(break_on_space[0]))
							flag = True
						else:
							flag = False
					else:
						flag = False


		# print("**********")
		# print(flag)
		if flag == True:
			if req_header:
				if ',' in req_header:
					req_header_splitter = req_header.split(",")
					for header in req_header_splitter:
						# print(header)
						req_header_re = re.compile(header)
						converted_reqHead_str = listToString(packet['request header'])
						# for element in packet['request header']:
							# print(element)
						if req_header_re.search(str(converted_reqHead_str)):
							matched_result.append("Matched_req_header: "+str(converted_reqHead_str))
							flag = True
							# break
						else:
							flag = False
				else:
					req_header_original = re.compile(req_header)
					# print("----")
					# print(req_header_original)
					converted_reqHead_str = listToString(packet['request header'])
					# print(converted_reqHead_str)
					# for element in packet['request header']:
						# print(element)
					if req_header_original.search(str(converted_reqHead_str)):
						matched_result.append("Matched_req_header: "+str(converted_reqHead_str))
						flag = True
						# break
					else:
						flag = False
					# for element in packet['request header']:
					# 	# print(element)
					# 	if req_header_original.search(str(element)):
					# 		matched_result.append("Matched_req_header: "+str(element))
					# 		flag = True
					# 		break
					# 	else:
					# 		flag = False

			# print(flag)
			if flag == True:
				if req_payload:
					if ',' in req_payload:
						req_payload_splitted = req_payload.split(',')

						for req_pay in req_payload_splitted:		
							req_pay_re = re.compile(req_pay)
							converted_reqPayload_str = listToString(packet['request payload'])
							# for element in packet['request payload']:
							if req_pay_re.search(str(converted_reqPayload_str)):
								matched_result.append("Matched_req_payload: "+str(converted_reqPayload_str))
								flag = True
								
							else:
								flag = False
					else:
						
						req_payload_orignal = re.compile(req_payload)
						converted_reqPayload_str = listToString(packet['request payload'])						
						# for element in packet['request payload']:
						if req_payload_orignal.search(str(converted_reqPayload_str)):

							matched_result.append("Matched_req_payload: "+str(converted_reqPayload_str))
							flag = True
							
						else:
							flag = False
						# for element in packet['request payload']:
						# 	if req_payload_orignal.search(str(element)):
						# 		matched_result.append("Matched_req_payload: "+str(element))
						# 		flag = True
						# 		break
						# 	else:
						# 		flag = False			

		if flag == True :
		
			# print(split_code)
			if resp_code:
				split_code = packet['response header'][0].split(" ")
				
				# print(resp_code)
				if resp_code.search(str(split_code[2])):
					# print("+++++++++++++++++++++++")
					# print(resp_code)
					matched_result.append("Matched_response_code: "+str(split_code[2]))
					flag = True
				else:
					flag = False

			if flag == True:
				if resp_header:
					if ',' in resp_header:
						resp_header_splitted = resp_header.split(',')
						for resp_head in resp_header_splitted:	
							resp_head_re = re.compile(resp_head)	
							converted_respHead_str = listToString(packet['response header'])	
							if resp_head_re.search(str(converted_respHead_str)):
								matched_result.append("Matched_response_header: "+str(converted_respHead_str))
								flag = True
							else:
								flag = False
					else:
						resp_header_original = re.compile(resp_header)
						converted_respHead_str = listToString(packet['response header'])
						if resp_header_original.search(str(converted_respHead_str)):
							matched_result.append("Matched_response_header: "+str(converted_respHead_str))
							flag = True
						else:
							flag = False



			if flag == True:	
				if resp_payload:
					# print(resp_payload)
					if ',' in resp_payload:
						resp_payload_splitted = resp_payload.split(',')
						
						for resp_pay in resp_payload_splitted:
							resp_pay_re = re.compile(resp_pay)	
							converted_respPayload_str = listToString(packet['response payload'])		
							if resp_pay_re.search(str(converted_respPayload_str)):
								matched_result.append("Matched_response_payload: "+str(converted_respPayload_str))
								flag = True
							else:
								flag = False
					else:
						resp_payload_original = re.compile(resp_payload)
						converted_respPayload_str = listToString(packet['response payload'])	
						if resp_payload_original.search(str(converted_respPayload_str)):
							matched_result.append("Matched_response_payload: "+str(converted_respPayload_str))
							flag = True
						else:
							flag = False


		if flag == True:
			found_flag_list.append("found")
			splitted_eq = eq.split(" ")
			print("Matched")
			matched_result.append("tcp.stream eq: "+str(splitted_eq[2]))
			# print("tcp.stream eq: "+str(splitted_eq[2]))
			final_results = matched_result

	# print(final_results)
	results = ''
	if 'found' in found_flag_list:
		if len(found_flag_list) == 1:
			#results = final_results
			pass
		else:
			results = ['Signature appear more than once ' ]
		
	else:
		results = ['Activity Unmatched']

	return results

with open('assembla_data') as f:
  data = json.load(f)
#
activities_lst = ['LOGIN', 'LOGIN-FAIL', 'LOGOUT', 'UPLOAD', 'DOWNLOAD', 'DELETE', 'SHARE', 'READ-ONLY']
#activities_lst = ['DELETE']
count= 0


files = os.listdir()
counter = 0
outer_dict = {}


for key, value in data.items():

		
	app_name = key.replace(".","").replace(" ","").replace('-','').replace("'", '')
	app_name = app_name.lower()


	for f in files:
		
		f_split = f.split('.pcap')
		file_name_split = f_split[0].split('_')

		pcap_file = ''
		packets_dict = {}


		# print(app_name)
		# if app_name == "odoopointofsale":
				# print("0000")

		# if hold2[0].find(app_name) != -1:
		if file_name_split[0] == value['custom_fields']['_Product_id']:
		# print(file_name_split)
		# if file_name_split[0] == str(53446):
		
			if  file_name_split[0] == value['custom_fields']['_Product_id'] :
				counter += 1
				print("Counter:		",counter, "........"," filename: ", f)
				
			# if value["Ticket_number"] == 1005:
				inner_dict = {}

				pcap_file = pyshark.FileCapture(f)
				packets_dict = open_pcap_packets(pcap_file, f)
				packets_dict = dict(sorted(packets_dict.items()))




				for activity in activities_lst:	
					
						
					if activity == 'LOGIN' or activity == 'LOGIN-FAIL' or activity == 'LOGOUT':
						if value["custom_fields"][activity+'_req-method'] != 'REMAINING' and value["custom_fields"][activity+'_req-method'] != 'NA' :
							result = pattern_matching(packets_dict, value ,activity, app_name)
							#print(activity)
							if len(result) > 0:
								inner_dict[activity] = result
							# pprint(result)
					else:
						if value["custom_fields"][activity+'_req-method'] != 'REMAINING' and value["custom_fields"][activity+'_req-method'] != 'NA':
							other_values = {}
							ls = []
							size, methods = multiple_values(value['custom_fields'][activity+'_req-method'],value['custom_fields'][activity+'_req-method-2'])
							result = ''
							# print(size)
							# print("------")
							
							if size > 1:
								host = separate_values(value['custom_fields'][activity+'_req-host'])
								uri = separate_values(value['custom_fields'][activity+'_req-uri-path'])
								param = separate_values(value['custom_fields'][activity+'_req-params'])
								req_header = separate_values(value['custom_fields'][activity+'_req-headers'])
								req_payload = separate_values(value['custom_fields'][activity+'_req-payload'])
								# print(req_payload)

								for i in range(size):
									if host:
										temp_host = host[i]
										
									if uri:
										temp_uri = uri[i]
									else: 
										temp_uri = ''
									
									if param:
										temp_param = param[i]
									else:
										temp_param = ''

									if req_header:
										temp_req_header = req_header[i]
									else:
										temp_req_header = ''

									if req_payload:
										temp_req_payload = req_payload[i]
										# print("=========+++========")
										# print(temp_req_payload)
									else:
										temp_req_payload = ''
									
									other_values['custom_fields']  ={ activity+"_req-method": methods[i], \
																	activity+'_req-host': temp_host, activity+'_req-uri-path': temp_uri, \
																	activity+'_req-params': temp_param, activity+'_req-headers':temp_req_header,\
																	activity+'_req-payload': temp_req_payload}

									ls.append({i : pattern_matching(packets_dict, other_values,activity, app_name)})
								if len(ls) > 0:
									inner_dict[activity] =  ls
								
							else:
								res= pattern_matching(packets_dict, value,activity,app_name)
								if len(res) > 0:
									inner_dict[activity]  = res

				outer_dict[key +" "+ value["Assigned to"]] = inner_dict

		with open ('Matched_Results_on_masterPcap_100.json', 'w') as outfile:
			json.dump(outer_dict, outfile, indent=4)

# pprint(outer_dict)
print("DONE..")



