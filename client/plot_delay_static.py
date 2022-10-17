import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# delay modify = average every x delay (x = 10, 50, 100)
# request rate r
r = 10
use_tm = 0
# data_name = '_tm1'
data_name = str(r)
simulation_time = 300  # 300 s
limit_cpus = 0.4
modify_ = 0  # choose avg delay
# tmp_str = "result2/result_cpu"
tmp_str = "k8s_result"
path = tmp_str + "/output10.txt"
path1 = tmp_str + "/output30.txt"
path2 = tmp_str + "/output50 .txt"
path3 = tmp_str + "/output_tm .txt"
# path3 = tmp_str + str(limit_cpus) + "/output100.txt"
# path4 = tmp_str + str(limit_cpus) + "/output_tm1.txt"
# path = "output" + str(data_name) + ".txt"
f = open(path, "r")
f1 = open(path1, "r")
f2 = open(path2, "r")
f3 = open(path3, "r")
# f4 = open(path4, "r")


if modify_:  # take average
    def cal_delay(f, use_tm, r, simulation_time):
        delay = []
        for line in f:
            # print(line)
            delay.append(float(line.rstrip('\n')) * 1000)
            # delay.append(float(line.rstrip('\n')) * 1000)
        f.close()

        # calculate  delay (ms)
        # print(len(delay))
        all_time = sum(delay)
        avg = sum(delay) / len(delay)
        max_d = max(delay)
        min_d = min(delay)
        print(avg, max_d, min_d)
        # max_d = 70

        request_num = []
        request_n = simulation_time
        if use_tm:
            f = open('request/request5.txt')

            for line in f:
                if len(request_num) < request_n:
                    request_num.append(int(float(line)))
        else:
            request_num = [r for i in range(simulation_time)]
        # print(request_num)
        # print(sum(request_num))

        delay_m = []
        count = 0

        for r in request_num:
            r = int(r)
            r_ = int(r / 2)
            tmp = delay[count:count + r]
            tmp = sorted(tmp, reverse=True)

            avg = sum(tmp[:r_]) / r_
            # max_ = max(tmp)

            if len(tmp) != 0:
                if tmp[0] > max_d - 20:
                    if tmp[0] > 50:
                        delay_m.append(max_d)
                    else:
                        delay_m.append(tmp[0])
                else:
                    delay_m.append(avg)

            # delay_m.append(avg)
            count += r
        return delay_m


    delay1 = cal_delay(f, use_tm, r, simulation_time)
    # delay2 = cal_delay(f1, use_tm, r, simulation_time)
    # delay3 = cal_delay(f2, use_tm, r, simulation_time)
    # delay4 = cal_delay(f3, 0, 100, simulation_time)
    # delay5 = cal_delay(f4, 1, 10, simulation_time)
    x1 = [i for i in range(300)]
    y1 = delay1
    # y2 = delay2
    # y3 = delay3
    # y4 = delay4
    # y5 = delay5
    Rmax = 15
    result1 = filter(lambda x: x > Rmax, y1)
    # result2 = filter(lambda x: x > Rmax, y2)
    # result3 = filter(lambda x: x > Rmax, y3)
    R1 = len(list(result1)) / len(y1)
    # R2 = len(list(result2)) / len(y2)
    # R3 = len(list(result3)) / len(y3)
    # print(R1, R2, R3)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x1, y=y1,
                             mode='lines',
                             name='Tmax30'))
    '''

    fig.add_trace(go.Scatter(x=x1, y=y2,
                             mode='lines',
                             name='Tmax40'))
    fig.add_trace(go.Scatter(x=x1, y=y3,
                             mode='lines',
                             name='Tmax50'))
    
    fig.add_trace(go.Scatter(x=x1, y=y4,
                        mode='lines',
                        name='100'))
    fig.add_trace(go.Scatter(x=x1, y=y5,
                        mode='lines',
                        name='workload5',
                        ))
    '''

    fig.update_layout(
        # title="Set request rate = " + str(r) + " requests/s",
        # title="Set request rate = workload4 ",
        # legend_title="Legend Title",

        xaxis_title="timestamp(s)",
        yaxis_title="Response time(ms)",
        font=dict(
            size=18
        )
    )

    fig.update_xaxes(range=[0, 300])
    fig.update_yaxes(range=[0, 100])
    fig.show()
    # fig.write_html("file.html")
    filename = "responsetime_" + str(limit_cpus) + ".png"
    fig.write_image(filename)

    # Plot real data----------------


def cal_real_delay(f, use_tm, r, simulation_time):
    delay = []
    for line in f:
        # print(line)
        delay.append(float(line.rstrip('\n')) * 1000)
        # delay.append(float(line.rstrip('\n')) * 1000)
    f.close()
    request_num = []
    request_n = simulation_time
    if use_tm:
        f = open('request/request5.txt')

        for line in f:
            if len(request_num) < request_n:
                request_num.append(int(float(line)))
    else:
        request_num = [r for i in range(simulation_time)]

    avg = sum(delay) / len(delay)
    max_d = max(delay)
    min_d = min(delay)
    print(avg, max_d, min_d)

    x = []
    count = 0
    for r in request_num:
        # print(r)
        d = 1 / r
        for i in range(r):
            x.append(count)
            # print(count)
            count += d

    y = delay

    return x, y


# f = open(path, "r")
# cal_real_delay(f, 0, 10, simulation_time)

x1, delay1 = cal_real_delay(f, use_tm, 10, simulation_time)
x2, delay2 = cal_real_delay(f1, use_tm, 30, simulation_time)
x3, delay3 = cal_real_delay(f2, use_tm, 50, simulation_time)
x4, delay4 = cal_real_delay(f3, 1, 50, simulation_time)
# delay4 = cal_delay(f3, 0, 100, simulation_time)
# delay5 = cal_delay(f4, 1, 10, simulation_time)
# x1 = [i for i in range(300)]
y1 = delay1
y2 = delay2
y3 = delay3
y4 = delay4
# y5 = delay5
# Rmax violation (%)
Rmax = 15
result1 = filter(lambda x: x > Rmax, y1)
result2 = filter(lambda x: x > Rmax, y2)
result3 = filter(lambda x: x > Rmax, y3)
result3 = filter(lambda x: x > Rmax, y4)
R1 = len(list(result1)) / 300
R2 = len(list(result2)) / 300
R3 = len(list(result3)) / 300
R4 = len(list(result3)) / 300
print(R1, R2, R3, R4)
# print(R1)
### plot delay

fig = go.Figure()

fig.add_trace(go.Scatter(x=x1, y=y1,
                         mode='lines',
                         name='10'))

fig.add_trace(go.Scatter(x=x2, y=y2,
                         mode='lines',
                         name='30'))
fig.add_trace(go.Scatter(x=x3, y=y3,
                         mode='lines',
                         name='50'))


fig.add_trace(go.Scatter(x=x1, y=y4,
                    mode='lines',
                    name='workload4'))

'''
fig.add_trace(go.Scatter(x=x1, y=y5,
                    mode='lines',
                    name='workload5',
                    ))
'''

fig.update_layout(
    # title="Set request rate = " + str(r) + " requests/s",
    # title="Set request rate = workload4 ",
    # legend_title="Legend Title",

    xaxis_title="timestamp(s)",
    yaxis_title="Response time(ms)",
    font=dict(
        size=18
    )
)

fig.update_xaxes(range=[0, 300])
fig.update_yaxes(range=[0, 100])
fig.show()
# fig.write_html("file.html")
filename = "responsetime_" + str(limit_cpus) + ".png"
fig.write_image(filename)
