import json 
from pprint import pprint


with open('JAN_results_on_individualpcaps_90.json','r') as f:
	matched_results = json.load(f)

with open('ticket_info_jan.json','r') as f:
	result = json.load(f)

activities_list = ['LOGIN','LOGIN-FAIL','LOGOUT','UPLOAD','DOWNLOAD','DELETE','SHARE','READ-ONLY']
eq = 0

# if os.path.isfile('http_first_request.txt'):
# 	http_first_request = read_file('http_first_request.json')
# else:
# 	http_first_request = {}

not_created_tcps = {}
count = 1
c = 0
login_dict = {}

for assem_key,value_assem in result.items():
	

	for key,value in matched_results.items():

		prod_id = assem_key
		app_name = value_assem['summary']
		c = c+1
		temp_app = key.split(' ')
		pname=key
		# if key.endswith('Hira Ahmed') or key.endswith('qazi ibrahim'):
		#     pname = ' '.join(temp_app[:-2])
		    
		# else:
		#     pname = ' '.join(temp_app[:-1])
		#print(pname)
		if pname == app_name:
			if 'LOGIN' in value:
				if 'Activity Unmatched' not in value['LOGIN'][0]:

					for v in value['LOGIN']:
						result = v.split(':')

						if result[0] == 'Matched_Req_Method':
							method = result[1]
						if result[0] == 'Matched_Host':
							host = result[1]+result[2]
						if result[0] == 'tcp.stream eq':
							eq_value = result[1]

							#print(prod_id)

							login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'LOGIN'+'!!!!'+'0'+'!!!!'+str(method.replace(' ',''))+' '+str(host)] = eq_value
			if 'LOGIN-FAIL' in value:
				if 'Activity Unmatched' not in value['LOGIN-FAIL'][0]:
					for v in value['LOGIN-FAIL']:
						fail_result = v.split(':')

						if result[0] == 'Matched_Req_Method':
							method = fail_result[1]
						if result[0] == 'Matched_Host':
							host = fail_result[1]+fail_result[2]
						if result[0] == 'tcp.stream eq':


							eq_value_fail = fail_result[1]
							

							login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'LOGIN-FAIL'+'!!!!'+'0'+'!!!!'+str(method.replace(' ',''))+' '+str(host)] = eq_value_fail
			if 'LOGOUT' in value:
				if 'Activity Unmatched' not in value['LOGOUT'][0]:
					for v in value['LOGOUT']:
						logout_result = v.split(':')

						if logout_result[0] == 'Matched_Req_Method':
							method = logout_result[1]
						if logout_result[0] == 'Matched_Host':
							host = logout_result[1]+logout_result[2]
						if logout_result[0] == 'tcp.stream eq':


							eq_value_fail = logout_result[1]
							

							login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'LOGOUT'+'!!!!'+'0'+'!!!!'+str(method.replace(' ',''))+' '+str(host)] = eq_value_fail

			if 'UPLOAD' in value:
				if 'Activity Unmatched' not in value['UPLOAD'][0]:

					for v in value['UPLOAD']:

						if type(v) is str:
							upload_result = v.split(':')

							if upload_result[0] == 'Matched_Req_Method':

								method = upload_result[1]
							if upload_result[0] == 'Matched_Host':
								host = upload_result[1]+upload_result[2]
							if upload_result[0] == 'tcp.stream eq':


								eq_value_fail = upload_result[1]
							

								login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'UPLOAD'+'!!!!'+'0'+'!!!!'+str(method.replace(' ',''))+' '+str(host)] = eq_value_fail

						
						if type(v) is dict:
							for v_key,v_value in v.items():
								#print(v_key)
								for inner_v in v_value:
									inner_v_upload = inner_v.split(':')
									
									if 'Activity Unmatched' not in inner_v_upload:
										if inner_v_upload[0] == 'Matched_Req_Method':
											method_upload = inner_v_upload[1]
										if inner_v_upload[0] == 'Matched_Host':
											host_inner = inner_v_upload[1]+inner_v_upload[2]
										if inner_v_upload[0] == 'tcp.stream eq':


											eq_value_fail_inner = inner_v_upload[1]
								

											login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'UPLOAD'+'!!!!'+v_key+'!!!!'+str(method_upload.replace(' ',''))+' '+str(host_inner)] = eq_value_fail_inner

			if 'DOWNLOAD' in value:
				if 'Activity Unmatched' not in value['DOWNLOAD'][0]:

					for v in value['DOWNLOAD']:
						print(v)

						if type(v) is str:
							download_result = v.split(':')

							if download_result[0] == 'Matched_Req_Method':

								method = download_result[1]
							if download_result[0] == 'Matched_Host':
								host = download_result[1]+download_result[2]
							if download_result[0] == 'tcp.stream eq':


								eq_value_fail = download_result[1]
							

								login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'DOWNLOAD'+'!!!!'+'0'+'!!!!'+str(method.replace(' ',''))+' '+str(host)] = eq_value_fail

						
						if type(v) is dict:
							for v_key,v_value in v.items():
								#print(v_key)
								for inner_v in v_value:
									inner_v_download = inner_v.split(':')
									
									if 'Activity Unmatched' not in inner_v_download:
										if inner_v_download[0] == 'Matched_Req_Method':
											method_download = inner_v_download[1]
							
										if inner_v_download[0] == 'Matched_Host':
										
											host_inner = inner_v_download[1]+inner_v_download[2]
										if inner_v_download[0] == 'tcp.stream eq':


											eq_value_fail_inner = inner_v_download[1]
								

											login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'DOWNLOAD'+'!!!!'+v_key+'!!!!'+str(method_download.replace(' ',''))+' '+str(host_inner)] = eq_value_fail_inner
			if 'DELETE' in value:
				if 'Activity Unmatched' not in value['DELETE'][0]:

					for v in value['DELETE']:

						if type(v) is str:
							delete_result = v.split(':')

							if delete_result[0] == 'Matched_Req_Method':

								method = delete_result[1]
							if delete_result[0] == 'Matched_Host':
								host = delete_result[1]+delete_result[2]
							if delete_result[0] == 'tcp.stream eq':


								eq_value_fail = delete_result[1]
							

								login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'DELETE'+'!!!!'+'0'+'!!!!'+str(method.replace(' ',''))+' '+str(host)] = eq_value_fail

						
						if type(v) is dict:
							for v_key,v_value in v.items():
								#print(v_key)
								for inner_v in v_value:
									inner_v_delete = inner_v.split(':')
									
									if 'Activity Unmatched' not in inner_v_delete:
										if inner_v_delete[0] == 'Matched_Req_Method':
											method_delete = inner_v_delete[1]
										
										if inner_v_delete[0] == 'Matched_Host':
										
											host_inner = inner_v_delete[1]+inner_v_delete[2]
										if inner_v_delete[0] == 'tcp.stream eq':


											eq_value_fail_inner = inner_v_delete[1]
								

											login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'DELETE'+'!!!!'+v_key+'!!!!'+str(method_delete.replace(' ',''))+' '+str(host_inner)] = eq_value_fail_inner

			if 'SHARE' in value:
				if 'Activity Unmatched' not in value['SHARE'][0]:

					for v in value['SHARE']:

						if type(v) is str:
							share_result = v.split(':')

							if share_result[0] == 'Matched_Req_Method':

								method = share_result[1]
							if share_result[0] == 'Matched_Host':
								host = share_result[1]+share_result[2]
							if share_result[0] == 'tcp.stream eq':


								eq_value_fail = share_result[1]
							

								login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'SHARE'+'!!!!'+'0'+'!!!!'+str(method.replace(' ',''))+' '+str(host)] = eq_value_fail

						
						if type(v) is dict:
							for v_key,v_value in v.items():
								#print(v_key)
								for inner_v in v_value:
									inner_v_share = inner_v.split(':')
									
									if 'Activity Unmatched' not in inner_v_share:
										if inner_v_share[0] == 'Matched_Req_Method':
											method_share = inner_v_share[1]
											
										if inner_v_share[0] == 'Matched_Host':
											
											host_inner = inner_v_share[1]+inner_v_share[2]
										if inner_v_share[0] == 'tcp.stream eq':


											eq_value_fail_inner = inner_v_share[1]
								

											login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'SHARE'+'!!!!'+v_key+'!!!!'+str(method_share.replace(' ',''))+' '+str(host_inner)] = eq_value_fail_inner

			if 'READ-ONLY' in value:
				if 'Activity Unmatched' not in value['READ-ONLY'][0]:

					for v in value['READ-ONLY']:

						if type(v) is str:
							read_only_result = v.split(':')

							if read_only_result[0] == 'Matched_Req_Method':

								method = read_only_result[1]
							if read_only_result[0] == 'Matched_Host':
								host = read_only_result[1]+read_only_result[2]
							if read_only_result[0] == 'tcp.stream eq':


								eq_value_fail = read_only_result[1]
							

								login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'READ-ONLY'+'!!!!'+'0'+'!!!!'+str(method.replace(' ',''))+' '+str(host)] = eq_value_fail

						
						if type(v) is dict:
							for v_key,v_value in v.items():
								#print(v_key)
								for inner_v in v_value:
									inner_v_read_only = inner_v.split(':')
									
									if 'Activity Unmatched' not in inner_v_read_only:
										if inner_v_read_only[0] == 'Matched_Req_Method':
											method_read_only = inner_v_read_only[1]
										
										if inner_v_read_only[0] == 'Matched_Host':
										
											host_inner = inner_v_read_only[1]+inner_v_read_only[2]
										if inner_v_read_only[0] == 'tcp.stream eq':


											eq_value_fail_inner = inner_v_read_only[1]
								

											login_dict[str(prod_id)+'!!!!'+str(pname)+'!!!!'+'READ-ONLY'+'!!!!'+v_key+'!!!!'+str(method_read_only.replace(' ',''))+' '+str(host_inner)] = eq_value_fail_inner

with open('http_file_eq_100.json','w') as outfile:
  	json.dump(login_dict, outfile,indent=4)



with open('http_file_eq_100.json','r') as file:
	final_result = json.load(file)	

final = {}

for key,value in final_result.items():
	final_value = value.replace(' ','')
	number="1" 
	if final_value != "0":
		print(value)  # 0 represents frst http request while 1 represents other than first 
		frst_request = final_value.replace(final_value,number)
	if final_value == "0":
		frst_request = final_value

	final[key] = frst_request

with open('http_request_first_file_Jan90.json','w') as file:
	json.dump(final,file,indent=4)



