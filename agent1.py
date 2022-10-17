import requests
from concurrent.futures import ThreadPoolExecutor
import time
import docker
import os
import threading
import pandas as pd


# delay modify = average every x delay (x = 10, 50, 100)
# request rate r
r = 1
use_tm = 1
T_max = 0.05  # 𝐓_𝒎𝒂𝒙  𝒗𝒊𝒐𝒍𝒂𝒕𝒊𝒐𝒏
# data_name = '_tm1'
data_name = '10'
simulation_time = 300  # 300 s
path = "output" + str(data_name) + ".txt"
request_num = []
request_n = simulation_time

if use_tm:
    f = open('request/request5.txt')

    for line in f:
        if len(request_num) < request_n:

            request_num.append(int(float(line)))
else:
    request_num = [r for i in range(simulation_time)]
print(request_num)


# request settings
f = open('request/request5.txt')
request_num = []
request_n = 3600
for line in f:
    if len(request_num) < request_n:

        request_num.append(int(float(line)))

# print(len(request_num))
# print(request_num)

# request_num = [1, 5, 10, 15, 50, 50, 100, 100, 500, 500, 1000, 1000, 5000, 5000]
# request_num = request_num[:1800]
request_num = [500]*8
# request_num = [1000]*100



def get_type(db_type):
    type1 = pd.DataFrame(list(db_type.find()))
    # print(type1['type'][0])
    type1 = type1['type'][0] # str
    return type1


def update_type(type1, type_c):
    myquery = {'type': type1}
    newvalues = {"$set": {'type': type_c}}
    db_type.update_many(myquery, newvalues)


def cal_cpu_percent(d):
    # cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    # cpu_count fix
    cpu_count = 16
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                   float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent


def get_url(url):
    myobj = {'num': 123}
    x = requests.post(url, data=myobj)

    # get_data = requests.get(url)
    final_time = time.time()
    alltime = final_time - start_time

    if alltime > 300:
        print('time:: ', alltime)
        exit()
    return x


def store_cpu():
    ## store_cpu
    for i in range(100000):
        time.sleep(0.01)
        client = docker.from_env()
        container1 = client.containers.get('service_1')
        d = container1.stats(stream=False)
        state_u = cal_cpu_percent(d)
        # print(state_u)
        mydict = {'cpu_u': state_u}
        db_cpu1.insert_one(mydict)


def send_con_request(url_type, type, start_time):
    type1 = get_type(db_type)
    for i in request_num:
        time.sleep(5)  # send requests every 5s
        list_of_urls = [url_type[0]] * i
        if type == '1':
            list_of_urls = [url_type[0]] * i
        if type == '2':
            list_of_urls = [url_type[0]] * int(i / 2) + [url_type[1]] * int(i / 2)
        if type == '3':
            list_of_urls = [url_type[0]] * int(i / 3) + [url_type[1]] * int(i / 3) + [url_type[2]] * int(i / 3)
        if type == '4':
            list_of_urls = [url_type[0]] * int(i / 4) + [url_type[1]] * int(i / 4) + [url_type[2]] * int(i / 4) + [url_type[3]] * int(i / 4)

        with ThreadPoolExecutor(max_workers=20) as pool:
            response_list = list(pool.map(get_url, list_of_urls))
            print(len(response_list))

        for response in response_list:
            # print(response)
            continue

def send_request(url_type, type, start_time):
    simulation_t = 1
    for i in request_num:
        # print(i)
        for j in range(i):

            get_url(url_type[0])
            time.sleep(1/i)  # send requests every 1s
        time.sleep(2)

    final_time = time.time()
    alltime = final_time - start_time
    print('time:: ', alltime)


def get_delay():
    type1 = get_type(db_type)
    while True:

        collection = list(db_delay1.find())
        data = pd.DataFrame(collection)
        r = data['123']
        # print('i =', i)
        try:

            ans = r[i]
            print(ans)
            i = i + 1
            return ans
        except:
            pass


def take_action():
    type1 = get_type(db_type)
    for i in range(100000):
        if type1 == '1':
            if get_delay() > 0.025:
                cmd = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 13 --name service_2 f2"
                os.system(cmd)
                time.sleep(1)
        if type1 == '2':
            if get_delay() > 0.025:
                cmd = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 13 --name service_2 f2"
                os.system(cmd)
                time.sleep(1)
        if type1 == '3':
            if get_delay() > 0.025:
                cmd = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 13 --name service_2 f2"
                os.system(cmd)
                time.sleep(1)


def take_action1(type1):
    global cpus
    for i in range(100000):
        if type1 == '1':
            cpus += 0.1
            if get_delay() > 0.05:
                cmd = "sudo docker update --cpus" + cpus + "service_1"
                os.system(cmd)
                time.sleep(1)




url1 = "http://172.17.0.2:5000/ping"
url2 = "http://172.17.0.3:5000/ping"
url3 = "http://172.17.0.4:5000/ping"
url4 = "http://172.17.0.5:5000/ping"

url_type = [url1, url2, url3, url4]
start_time = time.time()

cpus = 0.3

t1 = threading.Thread(target=send_request, args=(url_type, start_time, ))
t2 = threading.Thread(target=store_cpu)
t3 = threading.Thread(target=take_action)
t4 = threading.Thread(target=get_delay)
t1.start()
t2.start()
t3.start()

t4.start()




