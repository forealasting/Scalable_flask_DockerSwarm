import requests
from concurrent.futures import ThreadPoolExecutor
import time
import threading
from kubernetes import client, config

# f = open('request/request5.txt')
request_num = []
request_n = 300

cpus = 0.2  # initial cpus
if_nextrequest = 0
r = 30
use_tm = 1
simulation_time = 300

if use_tm:
    f = open('request/request5.txt')

    for line in f:
        if len(request_num) < request_n:

            request_num.append(int(float(line)))
else:
    request_num = [r for i in range(simulation_time)]

print(request_num)
print(len(request_num))

def get_url(url):
    myobj = {'num': 123}
    x = requests.post(url, data=myobj)

    # get_data = requests.get(url)
    # final_time = time.time()
    # alltime = final_time - start_time
    '''
    if alltime > 300:
        print('time:: ', alltime)
        exit()
    '''
    return x



start_time = time.time()
'''
for i in request_num:
    # time.sleep(5)  # send requests every 1s
    list_of_urls = [url]*i

    with ThreadPoolExecutor(max_workers=20) as pool:
        response_list = list(pool.map(get_url, list_of_urls))

    for response in response_list:
        # print(response)
        continue
    req_inx += 1
    print(len(response_list))
'''


def send_request(url_type, request_num):
    global change, send_finish
    global if_nextrequest

    for i in request_num:
        print(i)
        for j in range(i):

            get_url(url_type[0])
            time.sleep(1/i)  # send requests every 1s
        if_nextrequest += 1

    send_finish = 1


def store_cpu():
    global if_nextrequest, cpus


    while True:
        # time.sleep(0.1) // moniter period
        config.load_kube_config()
        api = client.CustomObjectsApi()
        resource = api.list_namespaced_custom_object(group="metrics.k8s.io", version="v1beta1", namespace="default",
                                                     plural="pods")
        data = list(resource["items"][-2]['containers'])
        cpu = data[0]['usage']['cpu']

        cpu = cpu.split('n')[0]
        cpu = int(cpu) / 10000000
        # print('cpu: ', cpu, " %")

        # print(state_u)
        path = "output_cpu" + str(r) + ".txt"
        final_time = time.time()
        t = final_time - start_time
        f = open(path, 'a')
        data = str(if_nextrequest) + ' ' + str(t) + ' ' + str(cpu) + ' ' + str(cpus) + '\n'
        f.write(data)
        f.close()



url1 = "http://192.168.49.2:31146/ping"
url2 = "http://192.168.49.2:32201/ping"

url_type = [url1, url2]


t1 = threading.Thread(target=send_request, args=(url_type, request_num, ))
t2 = threading.Thread(target=store_cpu, args=())

t1.start()
t2.start()

t1.join()
t2.join()