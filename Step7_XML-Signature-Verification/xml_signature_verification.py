import json 
from pprint import pprint

with open('sheet_data.json','r') as f:
	result = json.load(f)
	
activity_list = ['Login','Login_Fail','Logout','Upload','Download','Delete','Share','Read-Only']

final_xml = {}
counter = 0

for key,value in result.items():
	matched_activity = []
	for inner_key,inner_value in result.items():
		counter = counter + 1
			
		info_xml = {}
		count=0
		for activity in activity_list:
			
			for inner_activity in activity_list:

				xml_dict = {}
				


				string_to_match = value['GCActivity_'+activity+'_Signature_URL']

				dict_value_string = 'GCActivity_'+inner_activity+'_Signature_URL'

				string_to_match2 = inner_value[dict_value_string]


				if string_to_match!= 'NA' and string_to_match2 != 'NA' and string_to_match!= '' and string_to_match2 != '':


					if string_to_match == string_to_match2:


					

						if value['app_name'] != inner_value['app_name']:
							print('YES')

							comp = value['app_name']+'GCActivity_'+activity+'_Signature_URL '+'similiar to'+' '+inner_value['app_name']+' '+ dict_value_string
							
							count = count+1

			
							print(inner_value['app_name'])
							print(value['app_name'])
							xml_dict_key ='Match'+ str(count) + ' ' + inner_value['app_name']

							xml_dict['GCActivity_'+activity+'_Signature_URL'] = {'Activity':dict_value_string}
							# pprint(xml_dict)
							
							info_xml[xml_dict_key] = xml_dict

							pprint(info_xml)
							
							if value['app_name'] in final_xml.keys():


								final_xml[value['app_name']].update(info_xml)

							else:
								final_xml[value['app_name']] = info_xml


					

						if value['app_name'] == inner_value['app_name']:
						
							for same_activity in activity_list:
								
								
								if activity == same_activity:
								
									continue
								if activity != same_activity:
									
								
								
									string_to_match = value['GCActivity_'+activity+'_Signature_URL']

									dict_value_string = 'GCActivity_'+same_activity+'_Signature_URL'

									string_to_match2 = inner_value[dict_value_string]


									if string_to_match!= 'NA' and string_to_match2 != 'NA' and string_to_match!= '' and string_to_match2 != '':


										if string_to_match == string_to_match2:
											
											xml_dict_key ='Match'+ str(count) + ' ' + inner_value['app_name']

											xml_dict['GCActivity_'+activity+'_Signature_URL'] = {'Activity':dict_value_string}
											# pprint(xml_dict)
							
											info_xml[xml_dict_key] = xml_dict
											
											if value['app_name'] in final_xml.keys():


												final_xml[value['app_name']].update(info_xml)

											else:
												final_xml[value['app_name']] = info_xml


								
with open('XML_Errors.json','w') as f :
	json.dump(final_xml,f,indent=4)
