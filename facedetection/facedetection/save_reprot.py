import csv 
import time
from csv import DictWriter

# def save_report():
#     seconds = time.time()
#     local_time = time.ctime(seconds)
#     # The list of column names as mentioned in the CSV file
    
#     headersCSV = ['Name','status','time']      
#     # The data assigned to the dictionary 
    
#     with open('UN_reports.csv', 'a', newline='') as f_object:
#         # Pass the CSV  file object to the Dictwriter() function
#         # Result - a DictWriter object
#         dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
#         # Pass the data in the dictionary as an argument into the writerow() function
#         dictwriter_object.writerow(dict)
#         # Close the file object
#         f_object.close()

        
def save_report(name=None):
    seconds = time.time()
    local_time = time.ctime(seconds)
    # The list of column names as mentioned in the CSV file
    headersCSV = ['Name','status','time']      
    # The data assigned to the dictionary 
    if name:
        dict={'Name':f'{name}','status':'Drowsniess','time':f'{local_time}'}
    else:
        dict={'Name':"unknown person",'status':'unuthorized access','time':f'{local_time}'}
    with open('report.csv', 'a', newline='') as f_object:
        # Pass the CSV  file object to the Dictwriter() function
        # Result - a DictWriter object
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        # Pass the data in the dictionary as an argument into the writerow() function
        dictwriter_object.writerow(dict)
        # Close the file object
        f_object.close()