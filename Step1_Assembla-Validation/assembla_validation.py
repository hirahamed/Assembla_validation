#Requirement:
#make a creds_personal file for ticket access having access_key & access_secret
import json
from creds_personal import access_key, access_secret
from assembla import API,Ticket
import requests
from pprint import pprint
import re
import time

assembla_data = {}
app_names = {}
attachements = {}
def assembla_data_to_json(users, my_space, my_headers, drop2_tickets, drop3_tickets, drop4_tickets):
	ticket_ls = []
	count = 0
	for user_name in users:
		user = my_space.users(name=user_name)[0]
		print(user)
		for ticket in user.tickets():
			attachment_list_json = []
			attachments_temp = []
			attachement_names = []
			# print(ticket)
			if ticket['status'] == 'Pcap Checks' or ticket['status'] == 'Pcap Done' or ticket['status'] == 'XML Done':
				if ticket['custom_fields']['SaaS Validity'] == 'Yes' or ticket['custom_fields']['SaaS Validity'] == ' ':
					# if (not ticket['number'] in drop1_tickets) and (ticket['number'] in drop2_tickets):
					# if (not ticket['number'] in drop2_tickets) and (not ticket['number'] in drop3_tickets) :
					if ticket['number'] in drop4_tickets:
						count += 1
						
						ticket_number = ticket['number']
						# if ticket['status'] == ''
						ticket_ls.append(ticket_number)
						# print(ticket_number)
						# get attachements list through assembla api
						print("Fetching Assembla data.. Please wait...")
						space_name = "Granular-Controls"
						api = f'https://api.assembla.com/v1/spaces/{space_name}/tickets/{ticket_number}/attachments.json'
						# print(api)
						attachment_api_get = api	
						api_response = requests.get(attachment_api_get, headers=my_headers)
						response = api_response.text
						
						if len(response) > 0: 
							attachment_list_json = json.loads(api_response.text)
							for attachment in attachment_list_json:
								name = attachment['name'].split('.')
								# print(name)
								if name[-1] == 'pcap' or name[-1] == 'PCAP':
									attachments_temp.append(attachment_list_json)
									attachement_names.append(attachment['name'])
						else:
							attachement_names.append("Not found")
					
						# get assembla data through assembla wrapper 
						assembla_data[ticket['summary']] = { 'Assigned to':user_name, 'Ticket_number': ticket_number, 'Status': ticket['status'] ,'custom_fields': ticket['custom_fields'], 'Attachments_count': len(attachments_temp), 'Attachments_list':	attachement_names }
						# if ticket['status'] == 'Request for Info':
						# 	if len(attachment_list_json) >= 5:
						# 		app_names[ticket['summary']] = { 'Assigned to':user_name, 'Status': ticket['status'], 'Attachments_count': len(attachment_list_json)}
						attachements[ticket['summary']] = {'Assigned to':user_name, 'Attachments': attachement_names}

		# writing it to json file
		with open('available_tickets_drop4.json', 'w') as fp:  
			json.dump(ticket_ls,fp, indent = 1)

		print(count)
		# writing it to json file
		with open('assembla_data', 'w') as fp:  
			json.dump(assembla_data,fp,indent=1)

		# writing it to json file
		with open('attachments_pcaps', 'w') as fp:  
			json.dump(attachements,fp,indent=1)

def initial_validation(data, initial_errors):
	counter = 0
	initial_errors.clear()
	if not data['custom_fields']['HTTP-version']:
		initial_errors[counter] = "HTTP version not filled"
		counter += 1
		# print("key", app_name)
		# break
		

	if not data['custom_fields']['Personal'] and not data['custom_fields']['Corporate']:
		initial_errors[counter] = "Personal and Corporate both are empty, one of them should be filled"
		counter += 1

	if not data['custom_fields']['_Product_id']:
		initial_errors[counter] = "Product ID is missing"
		counter += 1

	return initial_errors



def login_and_login_fail_validation(data, activity_name, host_pattern, uri_pattern, login_loginFail_errors, activity_methods):
	activity_present = False
	counter = 0 
	login_loginFail_errors.clear()
	# print(activity_name)
		
	if (data['custom_fields'][activity_name+'_req-method'] != 'None') and (data['custom_fields'][activity_name+'_req-method'] != '')\
		 and (data['custom_fields'][activity_name+'_req-method'] != 'NA') and (data['custom_fields'][activity_name+'_req-method'] != 'REMAINING'):

		activity_present = True

		if data['custom_fields'][activity_name+'_req-method']:
			if not data['custom_fields'][activity_name+'_req-method'].lower() in activity_methods:
				login_loginFail_errors[counter] = " Request method value is incorrect"
				counter +=1

		if data['custom_fields'][activity_name+'_req-host']:
			
			if not host_pattern.search(data['custom_fields'][activity_name+'_req-host']):
				# print(data['custom_fields'][activity_name+'_req-host'])
				login_loginFail_errors[counter] = " Request host value seems to be incorrect"
				counter +=1
		else:
			login_loginFail_errors[counter] = " Host is missing"
			counter +=1

		if data['custom_fields'][activity_name+'_req-uri-path']:

			if not  uri_pattern.match(data['custom_fields'][activity_name+'_req-uri-path']):
				# print(data['custom_fields'][activity_name+'_req-uri-path'])
				login_loginFail_errors[counter] = " Request uri path value seems to be incorrect or starting '/' is missing(add /) or have space in starting(remove space)"
				counter +=1
		
		if data['custom_fields'][activity_name+'_req-headers']:
			if '|' in data['custom_fields'][activity_name+'_req-headers']:
				login_loginFail_errors[counter] = ' Error: Request header has pipe symbol, please replace it with comma'
				counter +=1


		if data['custom_fields'][activity_name+'_req-payload']:
			if '|' in data['custom_fields'][activity_name+'_req-payload']:
				login_loginFail_errors[counter] = ' Error: Request payload has pipe symbol, please replace it with comma'
				counter +=1

		if data['custom_fields'][activity_name+'_resp-header']:
			
			if '|' in data['custom_fields'][activity_name+'_resp-header']:
				# print(data['custom_fields'][activity_name+'_resp-header'])
				login_loginFail_errors[counter] = ' Error: Response header has pipe symbol, please replace it with comma'
				counter +=1

		if data['custom_fields'][activity_name+'_resp-payload']:
			if '|' in data['custom_fields'][activity_name+'_resp-payload']:
				login_loginFail_errors[counter] = ' Error: Response payload has pipe symbol, please replace it with comma'
				counter +=1

		if  uri_pattern.match(data['custom_fields'][activity_name+'_req-headers']):
			login_loginFail_errors[counter] = ' Request header value seems to be incorrect (found same pattern as uri path)'
			counter +=1

		if  uri_pattern.match(data['custom_fields'][activity_name+'_req-payload']):
			login_loginFail_errors[counter] = ' Request payload value seems to be incorrect (found same pattern as uri path)'
			counter +=1


		if  uri_pattern.match(data['custom_fields'][activity_name+'_resp-header']):
			login_loginFail_errors[counter] = ' Response header value seems to be incorrect (found same pattern as uri path)'
			counter +=1

		if  uri_pattern.match(data['custom_fields'][activity_name+'_resp-payload']):
			login_loginFail_errors[counter] = ' Response payload value seems to be incorrect (found same pattern as uri path)'
			counter +=1

		if  uri_pattern.match(data['custom_fields'][activity_name+'_resp-code']):
			login_loginFail_errors[counter] = ' response code value seems to be incorrect (found same pattern as uri path)'
			counter +=1

		if not data['custom_fields'][activity_name+'_resp-header'] and not data['custom_fields'][activity_name+'_resp-payload'] and not data['custom_fields'][activity_name+'_resp-code'] :
			# print(app_name)
			login_loginFail_errors[counter] =" Response not filled"
			counter +=1
			# print(login_loginFail_errors)

		if data['custom_fields'][activity_name+'_resp-code']:
			if not data['custom_fields'][activity_name+'_resp-code'].isdigit():
				# print(data['custom_fields'][activity_name+'_resp-code'])
				login_loginFail_errors[counter] =" Response code value is not integer"
				counter +=1

	if (data['custom_fields'][activity_name+'_req-method'] == 'None') or (data['custom_fields'][activity_name+'_req-method'] == ''):
		login_loginFail_errors[counter] = "Request method is empty, it should be filled"
		counter += 1

	if (data['custom_fields'][activity_name+'_req-method'] == 'NA') and (data['custom_fields'][activity_name+'_req-method'] == 'REMAINING'):
		if not data['custom_fields'][activity_name+'_req-host'] and not data['custom_fields'][activity_name+'_req-uri-path'] and \
			not data['custom_fields'][activity_name+'_req-params'] and not data['custom_fields'][activity_name+'_req-headers'] and \
			not data['custom_fields'][activity_name+'_req-payload'] and not data['custom_fields'][activity_name+'_resp-header'] and \
			not data['custom_fields'][activity_name+'_resp-payload']:
			pass
			# print(app_name)
			# print("all empty")
		else:
			login_loginFail_errors[counter] = "Request method is None/NA but all fields are not empty"
			counter += 1
			# print(login_loginFail_errors)
			# print("app name: ", app_name)
			# # break
			# pass
	
	return login_loginFail_errors, activity_present


def login_and_login_fail_depth(data, activity_name, params_depth_lst):
	params_depth_lst = []
	response = []

	if (data['custom_fields'][activity_name+'_req-method'] != 'None') and (data['custom_fields'][activity_name+'_req-method'] != '')\
		 and (data['custom_fields'][activity_name+'_req-method'] != 'NA') and (data['custom_fields'][activity_name+'_req-method'] != 'REMAINING'):

		if data['custom_fields'][activity_name+'_req-method']:
			params_depth_lst.append('_req-method')

		if data['custom_fields'][activity_name+'_req-host']:
			params_depth_lst.append('_req-host')
		
		if data['custom_fields'][activity_name+'_req-uri-path']:
			params_depth_lst.append('_req-uri-path')

		if data['custom_fields'][activity_name+'_req-params']:
			params_depth_lst.append('_req-params')

		if data['custom_fields'][activity_name+'_req-headers']:
			params_depth_lst.append('_req-headers')

		if data['custom_fields'][activity_name+'_req-payload']:
			params_depth_lst.append('_req-payload')

		if data['custom_fields'][activity_name+'_resp-code']:
			response.append('_resp-code')
			# params_depth_lst.append(activity_name+'_req-code')

		if data['custom_fields'][activity_name+'_resp-header']:
			response.append('_resp-header')

			# params_depth_lst.append(activity_name+'_req-header')

		if data['custom_fields'][activity_name+'_resp-payload']:
			response.append('_resp-payload')
			# params_depth_lst.append(activity_name+'_req-payload')
		
		if response:
			params_depth_lst.append(len(response))

	# print(params_depth_lst)
	return params_depth_lst


def logout_validation(data, activity_name, host_pattern, uri_pattern, logout_errors, activity_methods):
	counter = 0 
	activity_present = False

	if (data['custom_fields'][activity_name+'_req-method'] != 'None') and (data['custom_fields'][activity_name+'_req-method'] != '')\
		 and (data['custom_fields'][activity_name+'_req-method'] != 'NA') and (data['custom_fields'][activity_name+'_req-method'] != 'REMAINING'):

		activity_present = True
		if data['custom_fields'][activity_name+'_req-host']:
			if not host_pattern.search(data['custom_fields'][activity_name+'_req-host']):
				# print(data['custom_fields'][activity_name+'_req-host'])
				logout_errors[counter] = " Request host value seems to be incorrect"
				counter +=1
		else:
			logout_errors[counter] = " Host is missing"
			counter +=1

		if not data['custom_fields'][activity_name+'_req-method'].lower() in activity_methods:
			logout_errors[counter] = " Request method value is incorrect"
			counter +=1

		if data['custom_fields'][activity_name+'_req-uri-path']:

			if not uri_pattern.match(data['custom_fields'][activity_name+'_req-uri-path']):
				# print(data['custom_fields'][activity_name+'_req-uri-path'])
				logout_errors[counter] = " Request uri path value seems to be incorrect or starting '/' is missing(add /) or have space in starting(remove space)"
				counter +=1
		

		if data['custom_fields'][activity_name+'_response']:
			# print(app_name)
			logout_errors[counter] =" Response is filled, it should be empty"
			counter +=1
			# print(login_loginFail_errors)

		if  uri_pattern.match(data['custom_fields'][activity_name+'_req-headers']):
			logout_errors[counter] = ' Request header value seems to be incorrect (found same pattern as uri path)'
			counter +=1

		if  uri_pattern.match(data['custom_fields'][activity_name+'_req-payload']):
			logout_errors[counter] = ' Request header value seems to be incorrect (found same pattern as uri path)'
			counter +=1


	if (data['custom_fields'][activity_name+'_req-method'] == 'None') or (data['custom_fields'][activity_name+'_req-method'] == ''):
		logout_errors[counter] = "Request method is empty, it should be filled."
		counter += 1


	if (data['custom_fields'][activity_name+'_req-method'] == 'NA') or (data['custom_fields'][activity_name+'_req-method'] == 'REMAINING') :
		if not data['custom_fields'][activity_name+'_req-host'] and not data['custom_fields'][activity_name+'_req-uri-path'] and \
			not data['custom_fields'][activity_name+'_req-params'] and not data['custom_fields'][activity_name+'_req-headers'] and \
			not data['custom_fields'][activity_name+'_req-payload'] and not data['custom_fields'][activity_name+'_response']:
			pass
			# print(app_name)
			# print("all empty")
		else:
			logout_errors[counter] = "Request method is None but all fields are not empty"
			counter += 1

	
	return logout_errors, activity_present


def other_Acitivies_validation(data, activity_name, host_pattern, uri_pattern, other_activities_errors, activity_methods):
	counter = 0 
	activity_present = False
	other_activities_errors.clear()
	# print(data['custom_fields'][activity_name+'_req-method'])
	if (data['custom_fields'][activity_name+'_req-method'] != 'None') and (data['custom_fields'][activity_name+'_req-method'] != '')  \
		and (data['custom_fields'][activity_name+'_req-method'] != 'NA') and (data['custom_fields'][activity_name+'_req-method'] != 'REMAINING'):

		activity_present = True

		if not data['custom_fields'][activity_name+'_req-method'].lower() in activity_methods:
			other_activities_errors[counter] = " Request method value is incorrect"
			counter +=1


		if data['custom_fields'][activity_name+'_req-host']:

			if not host_pattern.search(data['custom_fields'][activity_name+'_req-host']):
				# print(":::::::::::::::::::::::")
				# print(host_pattern.search(data['custom_fields'][activity_name+'_req-host']))
				# print(data['custom_fields'][activity_name+'_req-host'])
				other_activities_errors[counter] = " Request host value seems to be incorrect"
				counter +=1

		else:
			other_activities_errors[counter] = " Host is missing"
			counter +=1

		if uri_pattern.match(data['custom_fields'][activity_name+'_req-params']):
			other_activities_errors[counter] = ' Params value seems to be incorrect (found same pattern as uri path)'
			counter +=1

		if  uri_pattern.match(data['custom_fields'][activity_name+'_req-headers']):
			other_activities_errors[counter] = ' Request header value seems to be incorrect (found same pattern as uri path)'
			counter +=1

		if uri_pattern.match(data['custom_fields'][activity_name+'_req-payload']):
			# print(data['custom_fields'][activity_name+'_req-payload'])
			other_activities_errors[counter] = ' Request payload value seems to be incorrect (found same pattern as uri path)'
			counter +=1

		if data['custom_fields'][activity_name+'_req-uri-path']:

			if not uri_pattern.match(data['custom_fields'][activity_name+'_req-uri-path']):
				# print(data['custom_fields'][activity_name+'_req-uri-path'])
				other_activities_errors[counter] = " Request uri path value seems to be incorrect or starting '/' is missing(add /) or have space in starting(remove space)"
				counter +=1
		

		if data['custom_fields'][activity_name+'_response']:
			# print(app_name)
			other_activities_errors[counter] =" Response is filled, it should be empty"
			counter +=1
			# print(login_loginFail_errors)

	
	if (data['custom_fields'][activity_name+'_req-method'] == 'None') or (data['custom_fields'][activity_name+'_req-method'] == ''):
		other_activities_errors[counter] = "Request method is empty, it should be filled."
		counter += 1

	if (data['custom_fields'][activity_name+'_req-method'] == 'NA') or (data['custom_fields'][activity_name+'_req-method'] == 'REMAINING'):
		if not data['custom_fields'][activity_name+'_req-host'] and not data['custom_fields'][activity_name+'_req-uri-path'] and \
			not data['custom_fields'][activity_name+'_req-params'] and not data['custom_fields'][activity_name+'_req-headers'] and \
			not data['custom_fields'][activity_name+'_req-payload'] and not data['custom_fields'][activity_name+'_response']:
			pass
			# print(app_name)
			# print("all empty")
		else:
			other_activities_errors[counter] = "Request method is None but all fields are not empty"
			counter += 1
			# print(login_loginFail_errors)
			# print("app name: ", app_name)
			# break
			pass

	
	return other_activities_errors, activity_present


def multiple_methods_validation(data, activity_name, multiple_methods_error , multiple_methods_err_lst, activity_methods):
	error_check = False 
	methods_ls = []
	if data['custom_fields'][activity_name+'_req-method'] != 'None' and data['custom_fields'][activity_name+'_req-method'] != '' and data['custom_fields'][activity_name+'_req-method'] != 'NA' and data['custom_fields'][activity_name+'_req-method'] != 'REMAINING':
		
		# if not ['custom_fields'][activity_name+'_req-method'] in activity_methods:
		# 	print("Req")

		methods_ls.append(data['custom_fields'][activity_name+'_req-method'])







		if data['custom_fields'][activity_name+'_req-method-2'] or ("|" in data['custom_fields'][activity_name+'_req-host']) or ("|" in data['custom_fields'][activity_name+'_req-uri-path']) or ("|" in data['custom_fields'][activity_name+'_req-params']) or ("|" in data['custom_fields'][activity_name+'_req-headers']) or ("|" in data['custom_fields'][activity_name+'_req-payload']):

			counter = 0
			value = data['custom_fields'][activity_name+'_req-method-2']
			methods_splitter = value.split('|')
			for methods in methods_splitter:
				methods_ls.append(methods)
			
			methods_ls_len = len(methods_ls)

			for method in methods_ls:
				if not method.lower() in activity_methods:
					multiple_methods_err_lst = " One or more request method values are incorrect "
					counter += 1
				
			if data['custom_fields'][activity_name+'_req-host']:
				value = data['custom_fields'][activity_name+'_req-host']
				hosts_splitter = value.split('|')

				if not (methods_ls_len == len(hosts_splitter)):
					error_check = True				

			if data['custom_fields'][activity_name+'_req-uri-path']:
				value = data['custom_fields'][activity_name+'_req-uri-path']
				uri_splitter = value.split('|')

				if not (methods_ls_len == len(uri_splitter)):
					error_check = True

			if data['custom_fields'][activity_name+'_req-params']:
				value = data['custom_fields'][activity_name+'_req-params']
				params_splitter = value.split('|')

				if not (methods_ls_len == len(params_splitter)):
					error_check = True

			if data['custom_fields'][activity_name+'_req-headers']:
				value = data['custom_fields'][activity_name+'_req-headers']
				req_header_splitter = value.split('|')

				if not (methods_ls_len == len(req_header_splitter)):
					error_check = True

			if data['custom_fields'][activity_name+'_req-payload']:
				value = data['custom_fields'][activity_name+'_req-payload']
				req_payload_splitter = value.split('|')

				if not (methods_ls_len == len(req_payload_splitter)):
					error_check = True


			if data['custom_fields'][activity_name+'_response']:
				value = data['custom_fields'][activity_name+'_response']
				response_splitter = value.split('|')

				if not (methods_ls_len == len(response_splitter)):
					error_check = True


	if error_check:
		multiple_methods_error = "Incorrect information against multiple methods"
	else: 
		multiple_methods_error = ""

	return multiple_methods_error, multiple_methods_err_lst

def multiple_values_validation(data, activity_name, multiple_values_error ):
	check = False
	multiple_values_error = ''
	values_length = []
	methods_ls = []
	max_len = 0

	if data['custom_fields'][activity_name+'_req-method'] != 'None' and data['custom_fields'][activity_name+'_req-method'] != '' and data['custom_fields'][activity_name+'_req-method'] != 'NA' and data['custom_fields'][activity_name+'_req-method'] != 'REMAINING' :
		
		
		methods_ls.append(data['custom_fields'][activity_name+'_req-method'])

		if data['custom_fields'][activity_name+'_req-method-2']:
			value = data['custom_fields'][activity_name+'_req-method-2']
			methods_splitter = value.split('|')
			for methods in methods_splitter:
				methods_ls.append(methods)
			
			# methods_ls_len = len(methods_ls)
			values_length.append( len(methods_ls))
			
		if data['custom_fields'][activity_name+'_req-host']:
			value = data['custom_fields'][activity_name+'_req-host']
		
			hosts_splitter = value.split('|')
			values_length.append(len(hosts_splitter))
			#hosts_ls.append(hosts_splitter)

			# if not (methods_ls_len == len(hosts_splitter)):
			# 	error_check = True				

		if data['custom_fields'][activity_name+'_req-uri-path']:
			value = data['custom_fields'][activity_name+'_req-uri-path']
			uri_splitter = value.split('|')
			#uri_ls.append(uri_splitter)
			values_length.append(len(uri_splitter))


			# if not (methods_ls_len == len(uri_splitter)):
			# 	error_check = True

		if data['custom_fields'][activity_name+'_req-params']:
			value = data['custom_fields'][activity_name+'_req-params']
			params_splitter = value.split('|')
			values_length.append(len(params_splitter))
			#params_ls.append(params_splitter)

			# if not (methods_ls_len == len(params_splitter)):
			# 	error_check = True

		if data['custom_fields'][activity_name+'_req-headers']:
			value = data['custom_fields'][activity_name+'_req-headers']
			req_header_splitter = value.split('|')
			values_length.append(len(req_header_splitter))
			# req_head_ls.append(req_header_splitter)

			# if not (methods_ls_len == len(req_header_splitter)):
			# 	error_check = True

		if data['custom_fields'][activity_name+'_req-payload']:
			value = data['custom_fields'][activity_name+'_req-payload']
			req_payload_splitter = value.split('|')
			values_length.append(len(req_payload_splitter))
			# req_payload_ls.append(req_payload_splitter)
			# if not (methods_ls_len == len(req_payload_splitter)):
			# 	error_check = True


		if data['custom_fields'][activity_name+'_response']:
			value = data['custom_fields'][activity_name+'_response']
			response_splitter = value.split('|')
			values_length.append(len(response_splitter))
			#response_ls.append(len(response_splitter))
			# if not (methods_ls_len == len(response_splitter)):
			# 	error_check = True
	

		if len(set(values_length)) != 1:
			check = True
			
		else: 
			check = False
		
		if len(values_length) > 1:
			max_len = max(values_length)
		elif len(values_length) == 1:
			max_len = 1
		else:
			max_len = 0

			
	if check:
		multiple_values_error = "Error: HTTP sessions depth not same"
	else: 
		multiple_values_error = ""

	return multiple_values_error, max_len


	# # if methods_ls
	
	# if error_check:
	# 	multiple_values_error = "Error: HTTP sessions depth not same"
	# else: 
	# 	multiple_values_error = ""

	# return multiple_values_error



def attachment_names_validation(attachments_names, activity_name, app_ticket, activity_count):
	lst = []
	validate_pcap = ''
	if activity_count == 0:
		validate_pcap = str(app_ticket)+"_"+activity_name+"-"+str(activity_count)
		if (validate_pcap+".pcap" in attachments_names) or (validate_pcap+".PCAP" in attachments_names):
			pass
			# lst.append("Correct fileName")
		else:
			print(validate_pcap)
			print(attachments_names)
			lst.append("Incorrect fileName")
	elif activity_count > 0:
		for i in range(activity_count):
			validate_pcap = str(app_ticket)+"_"+activity_name+"-"+str(i)
			# print(validate_pcap)
			if (validate_pcap+".pcap" in attachments_names) or (validate_pcap+".PCAP" in attachments_names):
				# lst.append("Correct fileName")
				pass
			else:
				lst.append("Incorrect fileName")
	
	return lst


# for assembla wrapper
assembla = API(
    key=access_key,
    secret=access_secret,
    # Auth details from https://www.assembla.com/user/edit/manage_clients
)

# for assembla api
my_headers = {'X-Api-Key' : access_key,
            'X-Api-Secret': access_secret,
            }

users = [ "qazi ibrahim", 'abdulrehman_29', 'adilaman', 'amnasherafal', 'Hira Ahmed','Maaz-Usmani',
		'maleehasiddiqui','ssalman', 'sundus_saleem', 'asad_qureshi', 'ShayanAqeel', "abdul_hayee"]
# users = ['Hira Ahmed']

activity_methods = ['delete', 'get', 'patch', 'post', 'put', 'remaining', 'na']

drop2_tickets = [707,21, 41, 98, 142, 143, 253, 275, 277, 278, 279, 281, 283, 285, 307, 313, 317, 320, 329, 371, \
	460, 499, 500, 503, 504, 517, 525, 526, 538, 549, 568, 597, 633, 663, 666, 702, 706, 7, 8, 84, 88, 111, 112, 114, \
	115, 127, 147, 148, 168, 179, 184, 190, 193, 229, 258, 294, 312, 328, 330, 336, 341, 346, 353, 357, 367, 386, 388, \
	399, 429, 430, 493, 505, 522, 523, 527, 530, 534, 535, 556, 572, 583, 616, 639, 704, 2, 3, 6, 9, 11, 13, 14, 16, 56, \
	62, 63, 67, 74, 82, 96, 101, 102, 107, 121, 130, 132, 198, 245, 270, 284, 296, 300, 315, 322, 325, 333, 351, 355, 358, \
	359, 370, 390, 397, 422, 435, 436, 441, 442, 454, 464, 469, 473, 475, 513, 524, 528, 532, 541, 548, 563, 569, 605, 606,\
	613, 617, 642, 651, 660, 662, 668, 670, 681, 17, 32, 33, 42, 58, 59, 64, 120, 156, 160, 224, 242, 246, 272, 310, 356, 362, \
	385, 387, 392, 401, 402, 405, 413, 414, 424, 426, 427, 440, 451, 455, 456, 459, 461, 463, 468, 472, 485, 497, 502, 520, 565, \
	638, 648, 10, 123, 126, 133, 136, 151, 173, 186, 189, 195, 196, 207, 210, 214, 225, 240, 247, 248, 251, 252, 259, 261, 301, 305, \
	314, 318, 331, 349, 350, 361, 364, 374, 375, 376, 409, 419, 431, 434, 450, 452, 480, 484, 537, 542, 543, 546, 552, 554, 555, 574, \
	577, 600, 608, 622, 631, 637, 645, 650, 661, 665, 667, 683, 694, 703, 5, 12, 15, 28, 29, 30, 31, 34, 35, 36, 37, 38, 39, 40, 70, 71, \
	77, 78, 86, 103, 113, 117, 216, 236, 327, 479, 489, 4, 45, 81, 87, 171, 211, 266, 332, 478, 491, 529, 551, 601, 609, 615, 619, 620, 700, \
	705, 18, 19, 20, 22, 24, 25, 26, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 60, 61, 66, 68, 69, 75, 76, 79, 80, 83, 85, 89, 90, 92, 93, 94, \
	95, 97, 99, 100, 104, 105, 106, 108, 110, 116, 118, 395]

#drop2_tickets = [721, 724, 725, 726, 742, 743, 767, 781, 803, 823, 825, 857, 859, 871, 873, 887, 888, 891, 918, 566, 570, 710, 713, 719, 732, 746, 750, 752, 762, 763, 766, 772, 775, 776, 785, 788, 814, 815, 816, 817, 818, 819, 839, 840, 841, 842, 843, 844, 875, 876, 881, 884, 885, 889, 897, 899, 901, 905, 908, 940, 709, 714, 715, 716, 730, 731, 733, 736, 738, 754, 759, 765, 783, 791, 792, 794, 795, 796, 799, 805, 810, 812, 834, 837, 838, 845, 848, 855, 861, 864, 866, 874, 878, 890, 892, 898, 902, 722, 728, 748, 751, 753, 757, 764, 768, 773, 774, 779, 797, 798, 807, 820, 829, 832, 851, 852, 860, 877, 883, 910, 917, 921, 945, 946, 953, 342, 366, 368, 453, 684, 718, 723, 729, 737, 739, 740, 744, 747, 749, 756, 770, 777, 780, 786, 793, 802, 809, 811, 813, 826, 835, 836, 846, 849, 850, 853, 854, 862, 867, 868, 869, 879, 880, 886, 893, 894, 895, 896, 904, 906, 919, 924, 927, 930, 932, 936, 720, 734, 735, 741, 745, 758, 761, 771, 782, 784, 789, 800, 806, 808, 821, 833, 847, 856, 865, 870, 872, 915, 920, 922, 701, 708, 711, 712, 727]

drop3_tickets = [1024, 1025, 1026, 1028, 1030, 1031, 1032, 1033, 1036, 1037, 1038, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1064, 1065, 1067, 1070, 1071, 1073, 1076, 1077, 1079, 1081, 1084, 1086, 1091, 1092, 1093, 1095, 72, 1096, 1097, 1098, 1099, 1101, 1104, 1106, 717, 243, 276, 790, 280, 288, 858, 900, 907, 911,	912, 914, 916, 926, 928, 929, 935, 937, 938, 939, 941, 943, 947, 949, 950, 951, 952, 954, 955, 956, 957, 958, 959, 961, 962, 963, \
	964, 965, 966, 967, 968, 969, 970, 971, 973, 975, 976, 977, 978, 979, 980, 982, 983, 984, 985, 986, 987, 988, 989, 990, 992, 993,994, 995, 997, 998, 999, 1000, 1001, 1002, 1003, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, \
	1018, 1020, 1021, 1022, 1023, 721, 724, 725, 726, 742, 743, 767, 781, 803, 823, 825, 857, 859, 871, 873, 887, 888, 891, 918, 566, 570, 710,713, 719, 732, 746, 750, 752, 762, 763, 766, 772, 775, 776, 785, 788, 814, 815, 816, 817, 818, 819, 839, 840, 841, 842, 843, 844, 875, 876, 881, 884, \
	885, 889, 897, 899, 901, 905, 908, 940, 709, 714, 715, 716, 730, 731, 733, 736, 738, 754, 759, 765, 783, 791, 792, 794, 795, 796, 799, 805, 810, 812, 834, 837, 838, 845, 848, 855, 861, 864, 866, 874, 878, 890, 892, 898, 902, 722, 728, 748, 751, 753, 757, 764, 768, 773, 774, 779, 797, 798, 807, 820, 829, 832, 851, 852, 860, 877, 883, 910, 917, 921, 945, 946, 953, 342, 366, 368, 453, 684, 718, 723, 729, 737, 739, 740, 744, 747, 749, 756, 770, 777, 780, 786, 793, 802, 809, 811, \
	813, 826, 835, 836, 846, 849, 850, 853, 854, 862, 867, 868, 869, 879, 880, 886, 893, 894, 895, 896, 904, 906, 919, 924, 927, 930, 932, 936, 720, 734, 735, 741,745, 758, 761, 771, 782, 784, 789, 800, 806, 808, 821, 833, 847, 856, 865, 870, 872, 915, 920, 922, 701, 708, 711, 712, 727]

drop4_tickets = [960, 972, 1063, 1078, 1120, 1125, 1126, 1127, 1131, 1133, 1134, 1135, 1136, 1139, 1145, 1149, 1159, 1160, 1181, 1182, 1183, \
	1186, 1189, 1193, 1204, 1208, 1217, 1221, 1229, 1236, 1250, 1257, 1270, 1279, 1285, 1294, 1068, 1083, 1087, 1088, 1094, 1107, 1119, 1121, \
		1122, 1123, 1124, 1132, 1151, 1154, 1157, 1166, 1167, 1175, 1177, 1178, 1179, 1195, 1201, 1202, 1206, 1209, 1211, 1218, 1220, 1226, 1253, \
			1271, 1284, 1291, 1292, 1019, 1089, 1102, 1103, 1105, 1115, 1138, 1142, 1143, 1144, 1150, 1161, 1162, 1187, 1190, 1191, 1192, 1194, 1207,\
	 1242, 1246, 1247, 1251, 1252, 1255, 1263, 1268, 1274, 1275, 1277, 1281, 1286, 1290, 1298, 1299, 1300, 1034, 1049, 1069, 1072, 1085, 1113, 1128, 1129, \
1140, 1147, 1156, 1171, 1174, 1180, 1188, 1198, 1200, 1203, 1237, 1240, 1256, 1276, 1280, 1289, 1080, 1082, 1090, 1100, 1110, 1111, 1112, 1118, 1130, 1141, \
1148, 1152, 1153, 1155, 1164, 1165, 1168, 1170, 1172, 1199, 1224, 1228, 1230, 1233, 1234, 1238, 1239, 1241, 1243, 1244, 1265, 1269, 1272, 1273, 1287, 1029, \
1066, 1074, 1075, 1108, 1109, 1114, 1116, 1117, 1146, 1158, 1163, 1169, 1176, 1185, 1197, 1205, 1210, 1232, 1235, 1248, 1262, 1264, 1267]

my_space= ''
while my_space == '':
	try:
		# To get data from assembla
		space_name='Granular Controls'
		my_space= assembla.spaces(name=space_name)[0]
		#print(len(my_space.tickets()))
		#below method call to hit the assembla api
		assembla_data_to_json(users, my_space, my_headers, drop2_tickets,drop3_tickets, drop4_tickets)
		break
	except:
		print("Connection refused by the server..")
		time.sleep(5)
		print("Was a nice sleep, now let me continue...")
		continue


with open('assembla_data') as f:
  data = json.load(f)


re_pattern_for_host = "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
host_pattern = re.compile(re_pattern_for_host)

re_pattern_for_uri =r"(^\/.*)"
uri_pattern = re.compile(re_pattern_for_uri)
user = {}


for app_name, value in data.items():


	error_logs = {}
	errors_dict = {}
	initial_errors = {}
	login_loginFail_errors = {}
	login_errors = {}
	login_file_error = {}

	loginFail_errors={}
	loginFail_file_error = {}

	logout_errors = {}
	logout_file_error = {}


	upload_errors = {}
	upload_multiple_methods_err = {}
	upload_multiple_methods_err_lst = {}
	upload_multiple_values_err = {}
	upload_file_error = {}

	download_errors = {}
	download_multiple_methods_err = {}
	download_multiple_methods_err_lst = {}
	download_multiple_values_err = {}
	download_file_error = {}

	delete_errors = {}
	delete_multiple_methods_err = {}
	delete_multiple_methods_err_lst = {}
	delete_multiple_values_err = {}
	delete_file_error = {}

	share_errors = {}
	share_multiple_methods_err = {}
	share_multiple_methods_err_lst = {}
	share_multiple_values_err = {}
	share_file_error = {}

	readonly_errors = {}
	readonly_multiple_methods_err = {}
	readonly_multiple_methods_err_lst = {}
	readonly_multiple_values_err = {}
	readonly_file_error = {}

	upload_values_count = 0
	download_values_count = 0
	delete_values_count = 0
	share_values_count = 0
	readonly_values_count = 0

	
	attachement_status = ""
	

	login_depth_lst = []
	loginFail_depth_lst = []

	activity_flag = False
	activies_present = []

	#if app_name == 'Sitefinity Digital Experience Cloud':
	if value['Status'] == 'Pcap Checks' or value['Status'] == 'Pcap Done' or value['Status'] == 'XML Done':
		initial_errors = initial_validation(value, initial_errors)

		activity_name = 'LOGIN'
		login_errors, activity_flag = login_and_login_fail_validation(value, activity_name, host_pattern, uri_pattern,login_errors, activity_methods)
		activies_present.append(activity_flag)
		login_depth_lst = login_and_login_fail_depth(value, activity_name, login_depth_lst)
		login_acitivty_count = 1
		if activity_flag:
			login_file_error = attachment_names_validation(value['Attachments_list'], activity_name, value['Ticket_number'], login_acitivty_count-1)
		# print("Login depth")
		# print(login_depth_lst )

		activity_name = 'LOGIN-FAIL'
		loginFail_errors, activity_flag = login_and_login_fail_validation(value, activity_name, host_pattern, uri_pattern, loginFail_errors, activity_methods)
		activies_present.append(activity_flag)
		loginFail_depth_lst = login_and_login_fail_depth(value, activity_name, loginFail_depth_lst)
		loginFail_acitivty_count = 1
		if activity_flag:
			loginFail_file_error = attachment_names_validation(value['Attachments_list'], activity_name, value['Ticket_number'], loginFail_acitivty_count-1)
		# print("Login-fail depth")
		# print(loginFail_depth_lst)
		# print((login_depth_lst))
		# print((loginFail_depth_lst))
		# if login_depth_lst == loginFail_depth_lst:
		# 	print('yesss')

		if login_depth_lst or loginFail_depth_lst:
			for x, y in zip(login_depth_lst, loginFail_depth_lst):
				if x != y:
					depth = "Failed: Incorrect depth between login and login-fail"
				else:
					depth = ""
		# print(depth)
		# if not (set(login_depth_lst) == set(loginFail_depth_lst)):
		# 	depth = "Failed: Incorrect depth between login and login-fail"
		# else:
		# 	depth = ""
		# print(depth)
		activity_name = 'LOGOUT'
		logout_errors, activity_flag = logout_validation(value, activity_name, host_pattern, uri_pattern, logout_errors, activity_methods)
		activies_present.append(activity_flag)
		logout_acitivty_count = 1
		if activity_flag:
			logout_file_error = attachment_names_validation(value['Attachments_list'], activity_name, value['Ticket_number'], logout_acitivty_count-1)
		# print(logout_errors)


		activity_name = 'UPLOAD'
		upload_errors, activity_flag = other_Acitivies_validation(value, activity_name, host_pattern, uri_pattern, upload_errors, activity_methods)
		activies_present.append(activity_flag)
		upload_multiple_methods_err, upload_multiple_methods_err_lst = multiple_methods_validation(value, activity_name, upload_multiple_methods_err,upload_multiple_methods_err_lst, activity_methods)
		upload_multiple_values_err, upload_values_count = multiple_values_validation(value, activity_name, upload_multiple_values_err)
		if activity_flag:
			upload_file_error = attachment_names_validation(value['Attachments_list'], activity_name, value['Ticket_number'], upload_values_count-1)



		activity_name = 'DOWNLOAD'
		download_errors, activity_flag = other_Acitivies_validation(value, activity_name, host_pattern, uri_pattern, download_errors, activity_methods)
		activies_present.append(activity_flag)
		download_multiple_methods_err, download_multiple_methods_err_lst = multiple_methods_validation(value, activity_name, download_multiple_methods_err, download_multiple_methods_err_lst, activity_methods)
		download_multiple_values_err, download_values_count = multiple_values_validation(value, activity_name, download_multiple_values_err)
		if activity_flag:
			download_file_error = attachment_names_validation(value['Attachments_list'], activity_name, value['Ticket_number'], download_values_count-1)

		# print(download_multiple_methods_err)


		activity_name = 'DELETE'
		delete_errors, activity_flag = other_Acitivies_validation(value, activity_name, host_pattern, uri_pattern, delete_errors, activity_methods)
		activies_present.append(activity_flag)
		delete_multiple_methods_err, delete_multiple_methods_err_lst = multiple_methods_validation(value, activity_name, delete_multiple_methods_err,  delete_multiple_methods_err_lst, activity_methods)
		delete_multiple_values_err, delete_values_count = multiple_values_validation(value, activity_name, delete_multiple_values_err)
		if activity_flag:
			delete_file_error = attachment_names_validation(value['Attachments_list'], activity_name, value['Ticket_number'], delete_values_count-1)


		# print(delete_multiple_methods_err)

		
		activity_name = 'SHARE'
		share_errors, activity_flag = other_Acitivies_validation(value, activity_name, host_pattern, uri_pattern, share_errors, activity_methods)
		activies_present.append(activity_flag)
		share_multiple_methods_err, share_multiple_methods_err_lst = multiple_methods_validation(value, activity_name, share_multiple_methods_err,  share_multiple_methods_err_lst, activity_methods)
		share_multiple_values_err, share_values_count = multiple_values_validation(value, activity_name, share_multiple_values_err)
		if activity_flag:
			share_file_error = attachment_names_validation(value['Attachments_list'], activity_name, value['Ticket_number'], share_values_count-1)

		# print(share_multiple_methods_err)

		activity_name = 'READ-ONLY'
		readonly_errors, activity_flag = other_Acitivies_validation(value, activity_name, host_pattern, uri_pattern, readonly_errors, activity_methods)
		activies_present.append(activity_flag)
		readonly_multiple_methods_err, readonly_multiple_methods_err_lst = multiple_methods_validation(value, activity_name, readonly_multiple_methods_err, readonly_multiple_methods_err_lst, activity_methods)
		readonly_multiple_values_err, readonly_values_count = multiple_values_validation(value, activity_name, readonly_multiple_values_err)
		if activity_flag:
			readonly_file_error = attachment_names_validation(value['Attachments_list'], activity_name, value['Ticket_number'], readonly_values_count-1)
		# print(readonly_multiple_methods_err)


		if len(initial_errors) > 0:
			errors_dict['Initial'] = initial_errors

		if len(login_errors) > 0:
			errors_dict['LOGIN'] = login_errors

		if len(login_file_error) > 0:
			errors_dict['LOGIN-Filename-Error'] = login_file_error


		if len(loginFail_errors) > 0:
			errors_dict['LOGIN-FAIL'] = loginFail_errors

		if len(loginFail_file_error) > 0:
			errors_dict['LOGIN-FAIL-Filename-Error'] = loginFail_file_error

		if depth:
			errors_dict['LOGIN_LOGIN-FAIL_DEPTH'] = depth

		if len(logout_errors) > 0:
			errors_dict['LOGOUT'] =logout_errors

		if len(logout_file_error) > 0:
			errors_dict['LOGOUT-Filename-Error'] = logout_file_error



		if len(upload_errors) > 0:
			errors_dict['UPLOAD'] =upload_errors

		if upload_multiple_methods_err:
			errors_dict['UPLOAD-MULTIPLE-METHODS'] =upload_multiple_methods_err

		if upload_multiple_methods_err_lst:
			errors_dict['UPLOAD-MULTIPLE-METHODS-VALIDATION'] =upload_multiple_methods_err_lst

		if upload_multiple_values_err:
			errors_dict['UPLOAD-MULTIPLE-VALUES'] =upload_multiple_values_err

		if len(upload_file_error) > 0:
			errors_dict['UPLOAD-Filename-Error'] = upload_file_error

		if len(download_errors) > 0:
			errors_dict['DOWNLOAD'] =download_errors

		if download_multiple_methods_err:
			errors_dict['DOWNLOAD-MULTIPLE-METHODS'] =download_multiple_methods_err

		if download_multiple_methods_err_lst:
			errors_dict['DOWNLOAD-MULTIPLE-METHODS-VALIDATION'] =download_multiple_methods_err_lst

		if download_multiple_values_err:
			errors_dict['DOWNLOAD-MULTIPLE-VALUES'] =download_multiple_values_err

		if len(download_file_error) > 0:
			errors_dict['DOWNLOAD-Filename-Error'] = download_file_error

		if len(delete_errors) > 0:
			errors_dict['DELETE'] =delete_errors

		if delete_multiple_methods_err:
			errors_dict['DELETE-MULTIPLE-METHODS'] =delete_multiple_methods_err

		if delete_multiple_methods_err_lst:
			errors_dict['DELETE-MULTIPLE-METHODS-VALIDATION'] =delete_multiple_methods_err_lst

		if delete_multiple_values_err:
			errors_dict['DELETE-MULTIPLE-VALUES'] =delete_multiple_values_err

		if len(delete_file_error)>0:
			errors_dict['DELETE-Filename-Error'] = download_file_error

		if len(share_errors) > 0:
			errors_dict['SHARE'] =share_errors

		if share_multiple_methods_err:
			errors_dict['SHARE-MULTIPLE-METHODS'] =share_multiple_methods_err

		if share_multiple_methods_err_lst:
			errors_dict['SHARE-MULTIPLE-METHODS-VALIDATION'] =share_multiple_methods_err_lst

		if share_multiple_values_err:
			errors_dict['SHARE-MULTIPLE-VALUES'] =share_multiple_values_err
		
		if len(share_file_error) > 0:
			errors_dict['SHARE-Filename-Error'] = share_file_error

		if len(readonly_errors) > 0:
			errors_dict['READ-ONLY'] =readonly_errors

		if readonly_multiple_methods_err:
			errors_dict['READ-ONLY-MULTIPLE-METHODS'] =readonly_multiple_methods_err

		if readonly_multiple_methods_err_lst:
			errors_dict['READONLY-MULTIPLE-METHODS-VALIDATION'] =readonly_multiple_methods_err_lst

		if readonly_multiple_values_err:
			errors_dict['READ-ONLY-MULTIPLE-VALUES'] =readonly_multiple_values_err

		if len(readonly_file_error) > 0 :
			errors_dict['READ-ONLY-Filename-Error'] = readonly_file_error

		if upload_values_count != 0:
			upload_count = upload_values_count - 1
		else:
			upload_count = upload_values_count

		if download_values_count != 0:
			download_count = download_values_count - 1
		else:
			download_count = download_values_count

		if delete_values_count != 0:
			delete_count = delete_values_count - 1
		else:
			delete_count = delete_values_count

		if share_values_count != 0:
			share_count = share_values_count - 1
		else:
			share_count = share_values_count

		if readonly_values_count != 0:
			readonly_count = readonly_values_count - 1
		else:
			readonly_count = readonly_values_count

		# checking if the attachment count is equal to the activities done
		overall_activities_count  = sum(activies_present) + upload_count + download_count + delete_count + share_count + readonly_count
		# print(app_name)
		# print(overall_activities_count)
		# print(value["Attachments_count"])
		# print(app_name)
		if overall_activities_count  == value["Attachments_count"]:
			attachement_status = ""
		else:
			attachement_status = "Failed: Incorrect number of attachments present against performed activities"
		
		if attachement_status:
			errors_dict['Attachements Status'] = attachement_status

		if len(errors_dict) > 0:
			# print(errors_dict)
			error_logs[app_name+" "+value['custom_fields']["_Product_id"]] = errors_dict

		key = value['Assigned to']
	
		if key not in user.keys():
			if error_logs:
				user[key] = error_logs	
		else:
			if error_logs:
				user[key].update(error_logs)

		print("Validating data... Please wait!!")


# # print(len(user))
# print(user)
for key, value in user.items():
	# print(key)
	# print(len(value))
	
	with open(key+'.json', 'w') as outfile:
		json.dump(value, outfile,indent=4)
	# pprint( list(user.keys()) )

# print(len(user))
#
