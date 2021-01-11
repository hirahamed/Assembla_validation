import os
import glob
import json

folders  = os.listdir()
count = 0

with open('assembla_data') as f:
  data = json.load(f)


for file_name in folders:
    # print(file_name)
    for app_name, value in data.items():
        app_name = app_name.replace("|"," ")
        if file_name != 'assembla_data' and not '.' in file_name:
            if int(file_name) == value['Ticket_number'] :
                print("yes")
                os.rename(file_name, value['custom_fields']['_Product_id']+" " + app_name)
        
            # if '.' in folder:
        #     hold = folder.split('.')
        #     print(hold)
        #     if not hold[-1] == 'py':
        #         print("IIIIIIIIIIIIII")

        #         os.rename(folder, "test "+str(count))
        #         count+=1
        # else:
        #     os.rename(folder, "test "+str(count))
        #     count+=1
# print(folders.name)
