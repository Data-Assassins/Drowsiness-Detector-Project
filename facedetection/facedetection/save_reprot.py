import csv
import time
# def save_report():
#     seconds = time.time()
#     local_time = time.ctime(seconds)
#     with open('reports.csv','w+') as f :
#         write = csv.writer(f)
#         f.write('Name = drowsniess ')
#         f.write('Status = drowsniess ')
#         f.write(f'Time = {local_time} \n')
# save_report()

def save_U_report(name):
    seconds = time.time()
    local_time = time.ctime(seconds)
    # yourName.append()
    with open('reports.csv', 'w', ) as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['Name','status','time'])
        wr.writerow([f'{name}','Drowsniess',f'{local_time}'])


def save_report():
    seconds = time.time()
    local_time = time.ctime(seconds)
    with open('UN_reports.csv', 'w', ) as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['Status','time'])
        wr.writerow(['unuthorized person',f'this {local_time}'])

