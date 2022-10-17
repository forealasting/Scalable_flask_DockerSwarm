from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

config.load_kube_config()
api = client.CustomObjectsApi()
resource = api.list_namespaced_custom_object(group="metrics.k8s.io", version="v1beta1", namespace="default", plural="pods")

for pod in resource["items"]:
    print(pod['containers'][0], "\n")
    print(pod['containers'][0]['name'])
'''
data = list(resource["items"][-2]['containers'])
cpu = data[0]['usage']['cpu']

cpu = cpu.split('n')[0]
cpu = int(cpu)/10000000
print('cpu: ', cpu, " %")
'''