import docker
client = docker.from_env()
# container = client.containers.run('flask', cpuset_cpus='15', cpu_count=0.2, name='service1234', auto_remove=True)
container = client.containers.get('b5d3')
stats1 = container.stats(stream=False)
top = container.top()
print(top)
print(list(stats1))
print(stats1['cpu_stats'])
