import requests
from concurrent.futures import ThreadPoolExecutor
import time
import docker
import os
import threading
import pandas as pd


# delay modify = average every x delay (x = 10, 50, 100)
# request rate r
r = 40
use_tm = 0
T_max = 0.03  # 𝐓_𝒎𝒂𝒙  𝒗𝒊𝒐𝒍𝒂𝒕𝒊𝒐𝒏
T_min = 0.01
set_tmin = 0  # 1 if setting tmin
cpus = 0.2  # initial cpus
simulation_time = 300  # 300 s
type = 1  # the nuber of containers
violation = []
request_num = []
request_n = simulation_time
change = 0
send_finish = 0
if_nextrequest = 0
if use_tm:
    f = open('request/request5.txt')

    for line in f:
        if len(request_num) < request_n:

            request_num.append(int(float(line)))
else:
    request_num = [r for i in range(simulation_time)]
print('lennnnn:: ', len(request_num))



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
    '''
    if alltime > 300:
        print('time:: ', alltime)
        exit()
    '''
    return x

# store cpu utilization and cpus
def store_cpu(start_time, service):
    global if_nextrequest, cpus

    ## store_cpu
    client = docker.from_env()
    container = client.containers.get(service)
    while True:
        # time.sleep(0.1) // moniter period

        d = container.stats(stream=False)
        state_u = cal_cpu_percent(d)
        # print(state_u)
        path = "output_cpu" + str(r) + ".txt"
        final_time = time.time()
        t = final_time - start_time
        f = open(path, 'a')
        data = str(if_nextrequest) + ' ' + str(t) + ' ' + str(state_u) + ' ' + str(cpus) + '\n'
        f.write(data)
        f.close()


def send_con_request(url_type, start_time):
    global type

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


def send_request(url_type, request_num, start_time):
    global change, send_finish
    global if_nextrequest

    for i in request_num:
        print(i)
        for j in range(i):

            get_url(url_type[0])
            time.sleep(1/i)  # send requests every 1s
        if_nextrequest += 1

        if change == 1:
            print('change!!!!')
            time.sleep(2)
            change = 0

    final_time = time.time()
    alltime = final_time - start_time
    print('time:: ', alltime)
    send_finish = 1


def get_delay():
    global type

    path = 'output_1.txt'
    try:
        f = open(path, "r")
        delay = []
        for line in f:
            delay.append(float(line.rstrip('\n')))
        # f.close()
        # print('max delay :: ', max(delay))
        # recent 10
        recent_max = max(delay[-15:])
        # print('recent max delay :: ', recent_max)
        return recent_max
    except:
        tmp_delay = 0
        print('cant open')
        return tmp_delay
    # print(delay[-1])

# add container
def take_action():
    global type

    for i in range(100000):
        if type == '1':
            if get_delay() > 0.025:
                cmd = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 13 --name service_2 f2"
                os.system(cmd)
                time.sleep(1)
        if type == '2':
            if get_delay() > 0.025:
                cmd = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 13 --name service_2 f2"
                os.system(cmd)
                time.sleep(1)
        if type == '3':
            if get_delay() > 0.025:
                cmd = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 13 --name service_2 f2"
                os.system(cmd)
                time.sleep(1)


# add cpu resource
def take_action1():
    global cpus, T_max, type, change, send_finish
    while(1):
        if send_finish == 1:
            break
        if type == 1:
            tmp_delay = get_delay()

            if tmp_delay > T_max and cpus < 1:
                cpus += 0.1
                cpus = round(cpus, 1)
                print('cps ::: ', cpus)
                cmd = "sudo docker update --cpus " + str(cpus) + " service_1"
                os.system(cmd)
                change = 1
                # print('change!!!!')
                time.sleep(5)
            if tmp_delay < T_min and cpus > 0.2 and set_tmin:
                cpus -= 0.1
                cpus = round(cpus, 1)
                print('cps ::: ', cpus)
                cmd = "sudo docker update --cpus " + str(cpus) + " service_1"
                os.system(cmd)
                change = 1
                # print('change!!!!')
                time.sleep(5)
    print('finish')

# sudo docker update --cpus 0.3 service_1
url1 = "http://172.17.0.2:5000/ping"
url2 = "http://172.17.0.3:5000/ping"
url3 = "http://172.17.0.4:5000/ping"
url4 = "http://172.17.0.5:5000/ping"

url_type = [url1, url2, url3, url4]
start_time = time.time()

t1 = threading.Thread(target=send_request, args=(url_type, request_num, start_time, ))
t2 = threading.Thread(target=store_cpu, args=(start_time, 'service_1',))
t3 = threading.Thread(target=take_action1)
# t4 = threading.Thread(target=get_delay)
t1.start()
t2.start()
t3.start()
# t4.start()

t1.join()
t2.join()
t3.join()
# t4.join()


