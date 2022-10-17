import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# delay modify = average every x delay (x = 10, 50, 100)
# request rate r
r = '30'
simulation_time = 300  # 300 s
if_store = 1
limit_cpus = 0.5
# tmp_str = "result2/result_cpu"
tmp_str = "k8s_result"
path = tmp_str + "/output_cpu10.txt"

path1 = tmp_str + "/output_cpu30.txt"
path2 = tmp_str + "/output_cpu50.txt"
path3 = tmp_str + "/output_cpu_tm.txt"

# path3 = tmp_str + str(limit_cpus) + "/tmp1/output_cpu100.txt"
# path4 = tmp_str + str(limit_cpus) + "/output_cputm1.txt"
# path = "output_cpu" + str(r) + ".txt"
f = open(path, "r")
f1 = open(path1, "r")
f2 = open(path2, "r")
f3 = open(path3, "r")
# f4 = open(path4, "r")

def cal_cpu(f, if_store):
    cpu = []
    time = []
    resource_use = []
    for line in f:
        s = line.split(' ')
        if float(s[2]) > 0:
            time.append(float(s[0]))
            cpu.append(float(s[2]))
            # resource_use.append(float(s[3]))
    f.close()

    # calculate  cpu (ms) ---------------

    # print(len(cpu))
    avg = sum(cpu) / len(cpu)
    max_d = max(cpu)
    min_d = min(cpu)
    print(avg, max_d, min_d)

    # calculate  cpu (ms) ---------------

    #
    x = 10
    cpu_m = []
    time_m = []

    for i, j in zip(time, cpu):

        if i <= 10000:

            time_m.append(i)
            cpu_m.append(j)
    # time_m = [x+1.5 for x in time_m]
    # time_m.insert(0, 0)
    # cpu_m.insert(0, 20)
    return time_m, cpu_m




# Plot --------------------------------------
x1, y1 = cal_cpu(f, 0)

x2, y2 = cal_cpu(f1, 0)

x3, y3 = cal_cpu(f2, 0)

x4, y4 = cal_cpu(f3, 0)

# x5, y5 = cal_cpu(f4, 1)

# d = {'timestamp(s)': x, 'Cpu utilization(%)': y}
# df = pd.DataFrame(d)
# x1 = [i for i in range(300)]
fig = go.Figure()

# fig = px.line(df, x='timestamp(s)', y='Cpu utilization(%)')
'''
fig.update_layout(
    # title="Set request rate = " + str(r) + " requests/s",
    title="Set request rate = workload4 ",
    # legend_title="Legend Title",
    font=dict(
        # family="Courier New, monospace",
        size=18,
        # color="RebeccaPurple"
    )
)
'''
fig.add_trace(go.Scatter(x=x1, y=y1,
                    mode='lines',
                    name='10'))

fig.add_trace(go.Scatter(x=x2, y=y2,
                    mode='lines',
                    name='30'))
fig.add_trace(go.Scatter(x=x3, y=y3,
                    mode='lines',
                    name='50'))

fig.add_trace(go.Scatter(x=x4, y=y4,
                    mode='lines',
                    name='workload4'))
'''
fig.add_trace(go.Scatter(x=x5, y=y5,
                    mode='lines',
                    name='workload5'))
'''
fig.update_layout(
    # title="Set request rate = workload4 ",
    # legend_title="Legend Title",
    xaxis_title="timestamp(s)",
    yaxis_title="Cpu utilization(%)",
    font=dict(
        size=20,
        # color="RebeccaPurple"
    )
)
fig.update_xaxes(range=[0, 300])
fig.update_yaxes(range=[0, 100])

fig.show()
filename = "cpu_utilization_" + str(limit_cpus) + ".png"
fig.write_image(filename)


# fig.write_html("file.html")
# Plot --------------------------------------


'''
# store if need
if if_store:

    path = 'output_cpu_u_m_' + str(r) + '.txt'
    f = open(path, 'a')
    for d in cpu_m:
        data = str(d) + '\n'
        f.write(data)
    f.close()

'''

''' # draw cpus 
res1.insert(0, 0.2)
res2.insert(0, 0.2)
res3.insert(0, 0.2)
# cal resource_use
fig = go.Figure()
fig.add_trace(go.Scatter(x=x1, y=res1,
                    mode='lines',
                    name='Tmax30'))


fig.add_trace(go.Scatter(x=x2, y=res2,
                    mode='lines',
                    name='Tmax40'))
fig.add_trace(go.Scatter(x=x3, y=res3,
                    mode='lines',
                    name='Tmax50'))

fig.update_layout(
    # title="Set request rate = workload4 ",
    # legend_title="Legend Title",
    xaxis_title="timestamp(s)",
    yaxis_title="cpus",
    font=dict(
        size=20,
        # color="RebeccaPurple"
    )
)
fig.update_xaxes(range=[0, 300])
fig.update_yaxes(range=[0, 1])

fig.show()
filename = "cpus" + str(limit_cpus) + ".png"
fig.write_image(filename)


res1_avg = sum(res1) / len(res1)
res2_avg = sum(res2) / len(res2)
res3_avg = sum(res3) / len(res3)
print(res1_avg)
print(res2_avg)
print(res3_avg)
'''