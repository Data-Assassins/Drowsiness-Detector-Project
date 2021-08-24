import csv
import time
from facedetection.face_detection import *

print(employee_names)

# def save_report():
#     seconds = time.time()
#     local_time = time.ctime(seconds)
#     with open('reports.csv','w+') as f :
#         write = csv.writer(f)
#         f.write('Name = drowsniess ')
#         f.write('Status = drowsniess ')
#         f.write(f'Time = {local_time} \n')
# save_report()
employee_names = f'{employee_names}'

def save_report():
    seconds = time.time()
    local_time = time.ctime(seconds)
    # yourName.append()
    with open('reports.csv', 'w', ) as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['Name','status','time'])
        for _ in employee_names:
            wr.writerow([f'test','Drowsniess',f'{local_time}'])
save_report()

