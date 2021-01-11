import json 
from pprint import pprint

with open('sheet_data.json','r') as f:
	result = json.load(f)
	
activity_list = ['Login','Login_Fail','Logout','Upload','Download','Delete','Share','Read-Only']

final_xml = {}

for key,value in result.items():
	matched_activity = []
	for inner_key,inner_value in result.items():
			
		info_xml = {}

		for activity in activity_list:
			
			for inner_activity in activity_list:

				xml_dict = {}
				count=0


				string_to_match = value['GCActivity_'+activity+'_Signature_URL']

				dict_value_string = 'GCActivity_'+inner_activity+'_Signature_URL'

				string_to_match2 = inner_value[dict_value_string]


				if string_to_match!= 'NA' and string_to_match2 != 'NA' and string_to_match!= '' and string_to_match2 != '':


					if string_to_match == string_to_match2:

					

						if value['app_name'] != inner_value['app_name']:
							print('YES')

							comp = value['app_name']+'GCActivity_'+activity+'_Signature_URL '+'similiar to'+' '+inner_value['app_name']+' '+ dict_value_string
							
							count = count+1
							xml_dict_key ='Match'+ str(count)

							xml_dict[xml_dict_key] = {'App_name':inner_value['app_name'],'Activity':dict_value_string}
							# pprint(xml_dict)
							
							info_xml['GCActivity_'+activity+'_Signature_URL'] = xml_dict
							# pprint(info_xml)
							
							final_xml[value['app_name']] = info_xml

					

						if value['app_name'] == inner_value['app_name']:
						
							for same_activity in activity_list:
								
								
								if activity == same_activity:
								
									continue
								if activity != same_activity:
									print(activity)
									print(same_activity)
								
								
									string_to_match = value['GCActivity_'+activity+'_Signature_URL']

									dict_value_string = 'GCActivity_'+same_activity+'_Signature_URL'

									string_to_match2 = inner_value[dict_value_string]


									if string_to_match!= 'NA' and string_to_match2 != 'NA' and string_to_match!= '' and string_to_match2 != '':


										if string_to_match == string_to_match2:
											
											xml_dict_key ='Match'+ str(count)

											xml_dict[xml_dict_key] = {'App_name':inner_value['app_name'],'Activity':dict_value_string}

								
											info_xml['GCActivity_'+activity+'_Signature_URL'] = xml_dict
								
											final_xml[value['app_name']] = info_xml

								
with open('XML_Errors.json','w') as f :
	json.dump(final_xml,f,indent=4)
