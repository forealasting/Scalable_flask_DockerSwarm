import docker
import os
import pymongo
client = pymongo.MongoClient("mongodb+srv://ncku_gwhsu:123@cluster0.wtz5pwg.mongodb.net/?retryWrites=true&w=majority")
db_cpu = client['state']['cpu_u1']


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


def take_action(state_u):
    if state_u > 0.4:
        cmd = "sudo docker update --cpus 0.6 service_1 "
        os.system(cmd)


client = docker.from_env()
container = client.containers.get('service_1')
d = container.stats(stream=False)
state_u = cal_cpu_percent(d)
print(state_u)

# take action
# take_action(state_u)






'''
stats = client.containers.get('service1').stats(stream=False)['cpu_stats']
print(stats)
print(type(stats))
'''
