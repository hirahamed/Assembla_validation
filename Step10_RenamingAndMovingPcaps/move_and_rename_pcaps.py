import os
import json

with open('assembla_data') as f:
  data = json.load(f)
#

files_list = os.listdir()
for f in files_list:
    name_split = f.split("_")
    print(name_split[0])
    for key,value in data.items():
        
        # print(value['Ticket_number'])
        if str(name_split[0]) == str(value['Ticket_number']) :
            app_name = key.replace(" ","")
            ending = "_".join(name_split[1:])
            output_file = app_name+"_"+str(ending)
            print(output_file)
            os.rename(f, output_file)
            print("renaming...")
            

    
