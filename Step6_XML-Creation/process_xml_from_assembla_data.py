from creds_personal import access_key
from creds_personal import access_secret
from assembla import API
from pprint import pprint
import collections
from dict2xml import dict2xml
import json,os
import csv 
import re
import glob

from xml.sax.saxutils import unescape

assembla = API(
    key=access_key,
    secret=access_secret,
)

SPACE_NAME='Granular Controls'
# my_space = assembla.spaces(name=SPACE_NAME)[0]

activities_list = ['LOGIN_','LOGIN-FAIL_','LOGOUT_','UPLOAD_','DOWNLOAD_','DELETE_','SHARE_','READ-ONLY_']

headers_mapping = collections.OrderedDict()
headers_mapping['req-method'] = 'http-req-method'

headers_mapping['req-method-2'] = 'http-req-method'

headers_mapping['req-uri-path'] = 'http-req-uri-path'
headers_mapping['req-params'] = 'http-req-params'
headers_mapping['req-host'] = 'http-req-host-header'
headers_mapping['req-headers'] = 'http-req-headers'


headers_mapping['req-payload'] = 'http-req-message-body'
headers_mapping['resp-code'] = 'http-rsp-code'
headers_mapping['resp-header'] = 'http-rsp-headers'
headers_mapping['resp-payload'] = 'panav-rsp-html-message-body'

#test_list = ['Change', 'DeftPDF', 'Square', 'ntile', 'AudioWeb', 'BitCopy', 'Arrangr', 'Skrill', 'Clara', 'Yahoo!', 'Microsoft', 'Nitro', 'SugarSync', 'github', 'SurveyCTO', 'Crowd', 'Lightspeed', 'LightSpeed', 'BookSimple', 'BookedIN', 'eEvid', 'bitbucket', 'ActiveInbox', 'Survey', 'GoDataFeed', 'HelloFax', 'Kickbox', 'Office', 'FeedbackFive', 'Zoho', 'Digital', 'Alternative', 'Pages', 'Lobbytrack', 'Zoho', 'hyper', 'Pingboard', 'Odoo', 'SurveyGizmo', 'Square', 'Formstack', 'Chili', 'Drupal', 'Ubiq', 'Knowee', 'Acuity', 'TimeTap', 'AppointmentXL', 'Envoy', 'SmartSurvey', 'Microsoft', 'Ecomchain', 'Bookafy', 'Datagame', 'Lipscore', 'ChannelApe', 'EasyEcom', 'Episerver', 'CheckMarket', 'BlueSnap', 'TowerData', 'Visme', 'easyDITA', 'My', 'SurveyLab', 'Keynote', 'GoCardless', 'SurveyLegend', 'dusupay', 'SelectPdf', 'Dwolla', 'Arcadier', 'Soda', 'Fusebill', 'Click2Sync', '3dcart', 'Ecwid', 'Square', 'InsiteCommerce', 'Dropbox', 'Doxami', 'OpenLM', 'Fraudhunt', 'Asana', 'Magento', 'Appoint.ly', 'Cart2Cart', 'Algopix', 'MailChannels', 'Chargebee', 'Startquestion', 'MsgSafe.io', 'Enalyzer', 'Gmail', 'VisibleThread', 'Live', 'CrazyLister', 'Threads', 'ARender', 'Google', 'Cronofy', 'NeverBounce', 'CoreUM', 'FLOW-e', 'Google', 'LinkedIn', 'Smaily', 'Nylas', 'QPoint', 'Google', 'ChargeOver', 'Zoom.ai', 'AmeriCommerce', 'SurveySparrow', 'Online', 'CS-Cart', 'mFax', 'Genbook', 'Microsoft', 'EmailMeForm', 'CS-Cart', 'Respondent', 'DataHawk.co', 'emaze', 'Calendly', 'SecurityMetrics', 'OroCommerce', 'IPQualityScore', 'edelpaper', 'Joysale', 'Swift', 'Loom', 'Pabbly', 'Mentimeter', 'Smallpdf', 'Spark', 'Notifii', 'Zappi', 'TinyTake', 'Zoho', 'Yelo', 'Servermx', '10to8', 'ActiveTextbook', 'Doofinder', 'HoneyBook', 'Multiorders', 'Feedier', '3DSellers', 'PDFShift', 'PayLane', 'Zoho', 'Zoho', 'Xverify', 'Apple', 'Twentify', 'Google', 'CoReceptionist', 'AbleCommerce', 'Microsoft', 'Apple', 'Scribd', 'iCal', 'AdZis', 'inkFrog', 'Nudgify', 'ProProfs', 'GoReminders', 'Oberlo', 'Clerk.io', 'Shopify', 'BigCommerce', 'eDesk', 'Braintree', 'Ve', 'FastSpring', 'SurveyFoxy', '2Checkout', 'Powtoon', 'Microsoft', 'Google', 'Zoho', 'MageNative', 'booxi', 'Easy', 'AddEvent', 'Harmonizely', 'ERPLY', 'Chrome', 'Swiftype', 'Snagshout', 'Unbxd', 'Patreon', 'MONEI', 'Zoho', 'Office', 'IPQualityScore', 'Square', 'AskCody', 'File', 'IMail', 'RingOver', 'Adobe', 'Bouncer', 'Microsoft', 'Cognito', 'Oliver', 'Greminders', 'Store', 'Unbxd', "Seller's", 'Pimcore', 'Timely', 'Nimble', 'Shoplo', 'Legalesign', 'Fingercheck', 'Zoho', 'HRMatrix', 'Salesbox', 'Sellbrite', 'Apptivo', 'Concord', 'Shoprocket', 'eSign', 'Proxyclick', 'HR', 'Capsule', 'OpenCart', 'PayWhirl', 'Helcim', 'Splitit', 'PipelineDeals', 'SalesVu', 'OnSched', 'Plytix', 'WordSynk', 'PyroCMS', 'Repsly', 'Hakema.io', 'GoCo', 'SuperSaaS', 'vcita', 'SignEasy', 'ProfitWell', 'Prysm', 'Printix', 'Primaseller', 'Skedda', 'Teamleader', 'Signority', 'Breathe', 'EKM', 'shopcloud', 'Salesmate', 'Price2Spy', 'The', 'SwipedOn', 'WhosOnLocation', 'AddressTwo', 'Mothernode', 'ONLYOFFICE', 'Voice', 'MonkeyData', 'ContractSafe', 'ContractZen', 'PurelyHR', 'Qminder', 'Namirial', 'E-Sign', 'amoCRM', 'DocVerify', 'Agile', 'Close', 'ScheduleOnce', 'Sharetribe', 'Teliver', 'Perzonalization', 'Miva', 'Leafinbox', 'Stripe', 'PayMotion', 'absence.io', 'Organimi', 'Socital', 'Typely', 'Conholdate.Total', 'Rising', 'Sellsy', 'Oneflow', 'ZeroBounce', 'Vendasta', 'Pinnacle', 'Square', 'SimplyBook.me', 'Setmore', 'Yotpo', 'BigContacts', 'SheerID', 'Easy', 'Sellbery', 'Awesome', 'Act!', 'Rezku', 'Staff', 'DigiSigner', 'Sales', 'Sertifi', 'Podia', 'pickatime', 'ResellerRatings', 'Qordoba', 'Handwrytten', 'Factorial', 'ASPEC', 'Volusion', 'x.ai', 'YouCanBook.me', 'ShopTab', 'Zoho', 'yocale', 'A2X', 'Copper', 'Vyte.in', 'SlickPOS', 'Stripe', 'Hypersay', 'OrgPlus', 'VisitUs', 'SignOnTheGo', 'Shopaccino', 'Eurecia', 'PIMworks', 'Data', 'Shipup', 'Iperius', 'Pin', 'SalezShark', 'PathFinder', 'Eval&GO', 'Glew', 'MangoPay', 'Vend', 'SureDone', 'Lextree', 'Xoyondo', 'Payeezy', 'PlagiarismCheck.org', 'QRCode', 'Stripe', 'Perpetua']

def read_file(file_name):
  
  # print("Reading file: " + file_name)
  with open(file_name) as json_file:
      result = json.load(json_file)
  return result

def write_file(data,file_name):
  
  print("Writing file: " + file_name)
  result = json.dumps(data, indent = 4)
  with open(file_name, 'w') as f:
    f.write(result)

def evaluate_empty(signature):
	if signature == '<and></and>':
		return 'NA'
	return signature

def evaluate_scope(sign):

	signatures = sign.split('!!!!')
	value = ''
	value_list = []
	for signature in signatures:
		if signature in ['NA','REMAINING','','<and></and>']:
			value = ''
		elif signature.find('http-rsp-code')!=-1 or signature.find('http-rsp-headers')!=-1 or signature.find('panav-rsp-html-message-body')!=-1:
			value = 'session'
		elif signature != '<and></and>':
			value = 'protocol-data-unit'
		else:
			value = 'SOME ISSUE'
		value_list.append(value)

	if len(value_list)>1:
		return '!!!!'.join(value_list)
	else:
		return value_list[0]

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('>', 'gt;'),
            ('<', '&lt;'),
            ('<', 'lt;'),
            ('', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


def evaluate_hs(appname,activity_name,sequence_no):



	json_ref_file = read_file('http_request_first_file_Jan100.json')
	search_key = '!!'+appname+'!!'
	http_record = [key for key, val in json_ref_file.items() if search_key in key]

	for hr in http_record:
		records = hr.split('!!!!')
		prod_id = records[0]
		prod_name = records[1]
		act_name = records[2]
		seq = records[3]
		sign = records[4]
		if act_name == activity_name and seq == sequence_no:
			return json_ref_file[hr] 
	
	return '1' #NEEDS TO BE FIXED AFTER

def get_hs(appname, activity_name,sign):

	signatures = sign.split('!!!!')
	value = ''
	value_list = []

	#Empty
	if sign == 'NA' or sign == 'REMAINING' or sign == '' or sign == '<and></and>':
		return ''
	
	#Multiple
	if len(signatures) > 1:
		for i in range(0,len(signatures)) :
			if signatures[i].find('http-req-message-body')!=-1 or signatures[i].find('http-rsp-code')!=-1 or signatures[i].find('http-rsp-headers')!=-1 or signatures[i].find('panav-rsp-html-message-body')!=-1:
				value_list.append('False')
			else:
				if evaluate_hs(appname,activity_name,str(i)) == '0':
					value_list.append('True')
				else:
					value_list.append('False')

		value = '!!!!'.join(value_list)
		
		return value

	#Single
	if signatures[0].find('http-req-message-body')!=-1 or signatures[0].find('http-rsp-code')!=-1 or signatures[0].find('http-rsp-headers')!=-1 or signatures[0].find('panav-rsp-html-message-body')!=-1:
		value = 'False'
	else:
		if evaluate_hs(appname,activity_name,'0') == '0':
			value = 'True'
		else:
			value = 'False'
	return value	

def evaluate_attachments(act_list):

	count = 0
	tcp = 0
	for i in act_list:
		if i == 'NA' or i=='':
			continue
		count = count + 1
		if i.find('!!!!') !=-1:
			temp0 = i.split('!!!!')
			tcp = tcp + len(temp0)
		else:
			tcp = tcp + 1
	return count,tcp


def write_csv():

	all_ticket_info = read_file('ticket_info.json')

	xml_info = read_file("xml_signatures.json")
	data_file = open('xml_signatures_to_sheet.csv', 'w') 
	csv_writer = csv.writer(data_file)
	extra_data = {}
	csv_writer.writerow([
						'product_id','product_name','correlation_urls','blocking_urls','Personal', 'Corporate','HTTP_version',
						'gcactivity_login_appid','gcactivity_login_isfirsthttprequest','gcactivity_login_scope','gcactivity_login_signatureurl',
						'gcactivity_loginfail_appid','gcactivity_loginfail_isfirsthttprequest','gcactivity_loginfail_scope','gcactivity_loginfail_signatureurl',
						'gcactivity_logout_appid','gcactivity_logout_isfirsthttprequest','gcactivity_logout_scope',	'gcactivity_logout_signatureurl',	
						'gcactivity_upload_appid','gcactivity_upload_isfirsthttprequest','gcactivity_upload_scope',	'gcactivity_upload_signatureurl',	
						'gcactivity_download_appid','gcactivity_download_isfirsthttprequest','gcactivity_download_scope','gcactivity_download_signatureurl',	
						'gcactivity_delete_appid','gcactivity_delete_isfirsthttprequest','gcactivity_delete_scope',	'gcactivity_delete_signatureurl',
						'gcactivity_share_appid','gcactivity_share_isfirsthttprequest','gcactivity_share_scope','gcactivity_share_signatureurl',	
						'gcactivity_readonly_appid','gcactivity_readonly_isfirsthttprequest','gcactivity_readonly_scope','gcactivity_readonly_signatureurl',
						'attachments','tcpcount'])

	for key,value in xml_info.items():
		product_name = value['product_name']
		http_version = value['HTTP_version']
		Personal = value['Personal']
		Corporate = value['Corporate']
		act_login = evaluate_empty(value['activities']['LOGIN_'])
		act_login_fail = evaluate_empty(value['activities']['LOGIN-FAIL_'])
		act_logout= evaluate_empty(value['activities']['LOGOUT_'])
		act_upload = evaluate_empty(value['activities']['UPLOAD_'])
		act_download = evaluate_empty(value['activities']['DOWNLOAD_'])
		act_delete = evaluate_empty(value['activities']['DELETE_'])
		act_share = evaluate_empty(value['activities']['SHARE_'])
		act_read_only = evaluate_empty(value['activities']['READ-ONLY_'])

		# print('LOGOUT ACTIVITY : ',act_logout)
		scp_login = evaluate_scope(value['activities']['LOGIN_'])
		scp_login_fail = evaluate_scope(value['activities']['LOGIN-FAIL_'])
		scp_logout= evaluate_scope(value['activities']['LOGOUT_'])
		scp_upload = evaluate_scope(value['activities']['UPLOAD_'])
		scp_download = evaluate_scope(value['activities']['DOWNLOAD_'])
		scp_delete = evaluate_scope(value['activities']['DELETE_'])
		scp_share = evaluate_scope(value['activities']['SHARE_'])
		scp_read_only = evaluate_scope(value['activities']['READ-ONLY_'])

		# print('LOGOUT SCOPE : ', scp_logout)

		hs_login = get_hs(product_name,'LOGIN' ,html_decode(act_login))
		hs_login_fail = get_hs(product_name, 'LOGIN-FAIL',html_decode(act_login_fail))
		hs_logout = get_hs(product_name, 'LOGOUT',html_decode(act_logout))
		hs_upload = get_hs(product_name, 'UPLOAD',html_decode(act_upload))
		hs_download = get_hs(product_name, 'DOWNLOAD',html_decode(act_download))
		hs_delete = get_hs(product_name, 'DELETE',html_decode(act_delete))
		hs_share = get_hs(product_name, 'SHARE',html_decode(act_share))
		hs_read_only = get_hs(product_name, 'READ-ONLY',html_decode(act_read_only))


		# print('hs_logout : ',hs_logout)
		attachments,tcp = evaluate_attachments([act_login,act_login_fail,act_logout,act_upload,act_download,act_delete,act_share,act_read_only])

		csv_writer.writerow([key,product_name,'','',Personal,Corporate,http_version,
							'',hs_login,scp_login,html_decode(act_login),
							'',hs_login_fail,scp_login_fail,html_decode(act_login_fail),
							'',hs_logout,scp_logout,html_decode(act_logout),
							'',hs_upload,scp_upload,html_decode(act_upload),
							'',hs_download,scp_download,html_decode(act_download),
							'',hs_delete,scp_delete,html_decode(act_delete),
							'',hs_share,scp_share,html_decode(act_share),
							'',hs_read_only,scp_read_only,html_decode(act_read_only),
							attachments,tcp]) 
		extra_data[product_name] = [attachments,tcp]
	# print('inques')
	# pprint(html_decode(act_upload))
	# print('inques55555555555555555555555555555555555555555555555555') 
	data_file.close() 
	print('Writing file: ' + 'xml_signatures_to_sheet.csv')
	write_file(extra_data,'extra_data.json')

def get_uri_from_json(activity_name,ticket_name,seq):

	json_ref_file = read_file('http_request_first_file_Jan100.json')
	search_key = '!!'+ticket_name+'!!'
	http_record = [key for key, val in json_ref_file.items() if search_key in key]
	# pprint(http_record)
	# print(len(http_record))

	for hr in http_record:
		infos = hr.split('!!!!')
		if activity_name == infos[2] + '_' and seq == infos[3]:
			return infos[3],infos[4]

	return None,None
		
def apply_space_start_and_end(test_str,context,activity_name,ticket_name,seq):

	if context not in ['http-req-host-header','http-req-uri-path']:
		return test_str

	proc = test_str
	if test_str.startswith('*'):
		proc = test_str.strip('*.')

	if test_str.endswith('*') or test_str.endswith('*/'):
		proc = '/'+test_str.strip('*/')+'/'

	if not test_str.startswith('*') and context in ['http-req-host-header']:
		proc = ' '+ proc

	if not test_str.endswith('*') or not test_str.endswith('*/') and context in ['http-req-uri-path']:
		number,signature = get_uri_from_json(activity_name,ticket_name,seq) #NEW added not tested
		if number == None or number != seq:
			# print('number : ', number)
			# print('sequence : ',seq)
			# print("YE THA ISSUE",signature)
			return ''
			return proc #THIS IS THE VERY BIG ISSUE IF XML NOT APPEARING
		if signature.find('?') ==-1:
			# print(signature.rsplit('/', 1)[-1])
			# print(test_str)
			# print(test_str.rsplit('/', 1)[-1])
			if signature.rsplit('/', 1)[-1] == test_str.rsplit('/', 1)[-1]:
				proc = proc + ' '

	# print(number)
	# print(signature)

	return proc

def process_pattern_for_special_characters(pattern):

	if pattern.find('.'):
		pp = pattern.split('.')
		return (r"\.".join(pp))
	else:
		return pattern

def patternmatch_for_xml_comma(key,processed_value,xml_tag,split_key_value,info_for_activity):

	patternmatch = collections.OrderedDict()
	patternmatch['pattern-match'] = collections.OrderedDict()
	if key.endswith('host'):
		patternmatch['pattern-match']['ignore-case'] = 'no'
		patternmatch['pattern-match']['pattern'] = processed_value.rstrip(' ')+'\\r\\n'
		patternmatch['pattern-match']['context'] = xml_tag 
		patternmatch['pattern-match']['qualifier-1'] =  info_for_activity.get(split_key_value[0]+'_req-method')
	else:
		patternmatch['pattern-match']['ignore-case'] = 'no'
		patternmatch['pattern-match']['pattern'] = processed_value
		patternmatch['pattern-match']['context'] = xml_tag

	return(patternmatch)

def patternmatch_for_xml_ast_in_bw(key,processed_value,xml_tag,split_key_value,info_for_activity):

	patternmatch = collections.OrderedDict()
	patternmatch['pattern-match'] = collections.OrderedDict()
	if key.endswith('host'):
		patternmatch['pattern-match']['ignore-case'] = 'no'
		patternmatch['pattern-match']['pattern'] = processed_value.rstrip(' ')+'\\r\\n'
		patternmatch['pattern-match']['context'] = xml_tag 
		patternmatch['pattern-match']['qualifier-1'] =  info_for_activity.get(split_key_value[0]+'_req-method')
	else:
		patternmatch['pattern-match']['ignore-case'] = 'no'
		patternmatch['pattern-match']['pattern'] = processed_value
		patternmatch['pattern-match']['context'] = xml_tag

	return(patternmatch)

def make_list_for_xml(entries,special):

	list_for_xml = []
	abc = collections.OrderedDict()

	if special == 1:
		list_for_xml.append({'entry':entries})
		return list_for_xml
	for i in entries:
		list_for_xml.append({'entry':i})
	return list_for_xml

def get_patternmatch_block(context,field_value,method):

	fv = field_value
	patternmatch = collections.OrderedDict()
	
	if context.endswith('host-header'):
		patternmatch['pattern-match'] = collections.OrderedDict()
		patternmatch['pattern-match']['ignore-case'] = 'no'
		patternmatch['pattern-match']['pattern'] = field_value.rstrip(' ')+'\\r\\n'
		patternmatch['pattern-match']['context'] = context 
		# patternmatch['pattern-match']['qualifier-1'] =  method
	elif context.endswith('req-method'):
		patternmatch['qualifier'] = collections.OrderedDict()
		patternmatch['qualifier']['entry'] = collections.OrderedDict()
		patternmatch['qualifier']['entry']['equal-to'] = collections.OrderedDict()
		patternmatch['qualifier']['entry']['equal-to']['field'] = context
		patternmatch['qualifier']['entry']['equal-to']['value'] = field_value
	elif context.endswith('rsp-code'):
		patternmatch['equal-to'] = collections.OrderedDict()
		patternmatch['equal-to']['field'] = context
		patternmatch['equal-to']['value'] = field_value
	else:
		patternmatch['pattern-match'] = collections.OrderedDict()
		patternmatch['pattern-match']['ignore-case'] = 'no'
		patternmatch['pattern-match']['pattern'] = field_value
		patternmatch['pattern-match']['context'] = context

	return(patternmatch)

def split_to_list(test_str,char):

	temp = test_str.split(char)
	proc_temp = []
	
	for i in temp:
		proc=i
		if proc.startswith('*'):
			proc = proc.strip('*.')

		if proc.endswith('*') or proc.endswith('*/'):
			proc = '/'+i.strip('*/')+'/'
		proc_temp.append(proc)
	
	return temp

def process_for_xs(fv,context,activity_name,ticket_name,method,seq):

	entries = []
	field_value_space = apply_space_start_and_end(fv,context,activity_name,ticket_name,seq)
	if field_value_space == '':
		return entries
	field_value_processed = process_pattern_for_special_characters(field_value_space)
	pm_block = get_patternmatch_block(context,field_value_processed,method)
	entries.append(pm_block)
	return entries

def get_xs_xml(method,host,contexts_for_activity,activity_name,ticket_name,seq):

	list_for_xml = []
	entries = []
	for context,field_value in contexts_for_activity.items():
		
		# if context == 'http-req-method':
		# 	continue

		if field_value == None or field_value == "":
			continue

		if field_value.find(',') != -1:
			fv_list = split_to_list(field_value,',')
			
			entries.append('<begin-orderfree/>')
			list_for_xml = make_list_for_xml(entries,1)

			for part in fv_list:
				if part.find('*') != -1:
					part_list = split_to_list(part,'*')
					for pl in part_list:
						if pl == '' or pl == '/':
							continue
						entries.append(process_for_xs(pl,context,activity_name,ticket_name,method,seq))
				else:
					if part == '' or part == '/':
							continue
					# pprint(entries)
					entries.append(process_for_xs(part,context,activity_name,ticket_name,method,seq))
			
			entries.append('<end-orderfree/>')
			list_for_xml = make_list_for_xml(entries,1)

		elif field_value.find('*') != -1:
			if context == 'http-req-host-header':
				# print("------------------------------------------------------")
				# print(field_value)
				part_list = [field_value]
			else:
				part_list = split_to_list(field_value,'*')
			for pl in part_list:
				if pl == '' or pl =='/':
					continue
				entries.append(process_for_xs(pl,context,activity_name,ticket_name,method,seq))
		else:
			if context == 'http-req-host-header':
				entries.append(process_for_xs(host,context,activity_name,ticket_name,method,seq))
			else:
				if field_value == '' or field_value == '/':
					continue
				entries.append(process_for_xs(field_value,context,activity_name,ticket_name,method,seq))

	# print("THESE ARE ENTRIES")
	# pprint(entries)
	# alist = [[],[]]
	if not any(entries):
	    print("Empty list!")
	    entries = []
	
	list_for_xml = make_list_for_xml(entries,0)
	# xml_snippet = '<and>' + dict2xml(list_for_xml) + '</and>'
	# print(xml_snippet)
	xml_snippet = dict2xml(list_for_xml,indent='',newlines=False)
	# xml_snippet = dict2xml(list_for_xml,indent='',newlines=True)
	# pprint(xml_snippet)
	# xml_snippet = '<and>' + dict2xml(list_for_xml) + '</and>'
	# print(xml_snippet)
	return xml_snippet

def process_for_http_sessions(contexts_for_activity,activity_name,ticket_name):

	list_for_xml = []
	entries = []

	methods = split_to_list(contexts_for_activity['http-req-method'],'|')
	hosts = split_to_list(contexts_for_activity['http-req-host-header'],'|')
	context_dict = collections.OrderedDict()
	xml_snippet = ''

	for i in range(0,len(methods)):
		host = hosts[i]
		method = methods[i]

		for key,value in contexts_for_activity.items():
			# if key in ['http-req-method','http-req-host-header']:
			# 	continue
			temp_value = split_to_list(contexts_for_activity[key],'|')
			context_dict[key]=temp_value[i]	
		context_dict['http-req-method']=method
		context_dict['http-req-host-header']=host

		list_for_xml = get_xs_xml(method,host,context_dict,activity_name,ticket_name,str(i))
		if i+1 != len(methods):
			xml_snippet = xml_snippet + '<and>' + dict2xml(list_for_xml,indent='',newlines=False)  + '</and>' + '!!!!'
			# xml_snippet = xml_snippet + '<and>' + dict2xml(list_for_xml,indent='',newlines=True)  + '</and>' + '!!!!'
		else:
			xml_snippet = xml_snippet + '<and>' + dict2xml(list_for_xml,indent='',newlines=False)  + '</and>'
			# xml_snippet = xml_snippet + '<and>' + dict2xml(list_for_xml,indent='',newlines=True)  + '</and>'
	# pprint(xml_snippet)
	return xml_snippet


def prepare_data_from_assembla(info_for_activity,activity_name,ticket_name):

	context = collections.OrderedDict()
	
	if activity_name in ['LOGIN_','LOGIN-FAIL_','LOGOUT_']:
		info_for_activity.pop(activity_name+'req-method-2', None)

	if activity_name not in ['LOGIN_','LOGIN-FAIL_']:
		info_for_activity.pop(activity_name+'resp-code', None)

	for key,value in info_for_activity.items():
		field_value = ''

		if value == None or value == "":
			continue

		split_key = key.split('_')

		if split_key[1] == 'req-method-2' or split_key[1] == 'req-method': #only for req method2
			if (split_key[0]+'_'+'req-method-2') in info_for_activity:
				if info_for_activity[split_key[0]+'_'+'req-method-2'] != '':
					field_value = info_for_activity[split_key[0]+'_'+'req-method'] + '|' + info_for_activity[split_key[0]+'_'+'req-method-2']
				else:
					field_value = value
			else:
				field_value = info_for_activity[split_key[0]+'_'+'req-method']
		else:
			field_value = value
		
		context[headers_mapping.get(split_key[1])]=field_value
	return process_for_http_sessions(context,activity_name,ticket_name)

def get_xml_signature_per_activity(ticket_info,ticket_name):

	activities = collections.OrderedDict()
	headers = list(headers_mapping.keys())
	for a in range(0,len(activities_list)):

		# if activities_list[a] != 'DELETE_':
		# 	continue

		info_for_activity = collections.OrderedDict()
		for h in headers:
			key = activities_list[a]+h
			value = ticket_info.get(key)
			info_for_activity[key] = value

		if info_for_activity[activities_list[a]+'req-method'] in ['REMAINING']:
			activities[activities_list[a]] = ''
			continue
		if info_for_activity[activities_list[a]+'req-method'] in ['NA','']:
			activities[activities_list[a]] = 'NA'
			continue

		activities[activities_list[a]] = prepare_data_from_assembla(info_for_activity,activities_list[a],ticket_name)

	return activities

def get_xml_all_signatures():
	
	xml_signatures = collections.OrderedDict()
	all_ticket_info = read_file('ticket_info.json')

	#100 apps product ids
	prod_list = ['100413', '103137', '10819', '111112', '111113', '13817', '14005', '14848', '1531', '15860', '1588', '1589', '1593', '1610', '1619', '1626', '1668', '1711', '1744', '1841', '18503', '19183', '19345', '19359', '1960', '19665', '19711', '20659', '20852', '20994', '2179', '22283', '24641', '25279', '25583', '2627', '26332', '2642', '2650', '2668', '269', '2701', '27035', '27119', '27406', '27569', '2794', '2863', '29352', '3204', '3215', '324', '3526', '36330', '37240', '37316', '3778', '39638', '39729', '40474', '40629', '42183', '42313', '43491', '44599', '4748', '49502', '49867', '49879', '506', '50878', '5164', '53164', '53980', '541', '54586', '5545', '5653', '5753', '576', '57927', '59281', '6203', '62145', '66947', '674', '67442', '69214', '7113', '71881', '73153', '76356', '770', '8308', '8631', '87264', '90218', '922', '96837', '99259']
	# prod_list = ['25557']
	for key,value in all_ticket_info.items():
		
		if key not in prod_list:
			continue
		
		xml_signatures[key] ={
								'product_name':value['summary'] ,
								'Personal': value["custom_fields"]["Personal"],
								"Corporate": value["custom_fields"]["Corporate"],
								'HTTP_version' :  value['custom_fields']['HTTP-version'],
							    'activities':get_xml_signature_per_activity(value['custom_fields'],value['summary']),
							    'ticket_no':value['ticket_no']
							   }
	pprint(xml_signatures)
	write_file(xml_signatures,'xml_signatures.json')

def get_ticket_info():
	
	my_space = assembla.spaces(name=SPACE_NAME)[0]
	all_tickets = my_space.tickets()

	ticket_info = {}
	count = 0

	for ticket in my_space.tickets():
		if ticket['status'] not in ['Pcap Done','Pcap Checks','XML Done']:
			continue
		if ticket['custom_fields']['SaaS Validity'] == 'No':
			continue
		count = count + 1
		ticket_info[ticket['custom_fields']['_Product_id']] = {
	    								'summary':ticket['summary'],
	    								'custom_fields' : ticket['custom_fields'],
	    								'ticket_no' : ticket['number']

	    								}

	write_file(ticket_info,'ticket_info.json')

def main():

    # get_ticket_info()
    get_xml_all_signatures()
    write_csv()

if __name__ == "__main__":
    main()
