import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# dynamic workload

path = "request5.txt"
f = open(path, "r")
request = []
for line in f:
    data = int(line)
    request.append(data)
f.close()


x = [i for i in range(300)]
y0 = [10 for i in range(300)]
y1 = [30 for i in range(300)]
y2 = [50 for i in range(300)]
# y3 = [100 for i in range(300)]
y4 = request

fig = go.Figure()
# fig = px.line(df, x='Simulation time(s)', y='Data rate(requests/s)')
fig.add_trace(go.Scatter(x=x, y=y0,
                    mode='lines',
                    name='workload1'))
fig.add_trace(go.Scatter(x=x, y=y1,
                    mode='lines',
                    name='workload2'))
fig.add_trace(go.Scatter(x=x, y=y2,
                    mode='lines',
                    name='workload3'))

# fig.add_trace(go.Scatter(x=x, y=y3,
#                    mode='lines',
#                    name='workload4'))
fig.add_trace(go.Scatter(x=x, y=y4,
                    mode='lines',
                    name='workload4'))

fig.update_layout(
    title="Workload",
    # legend_title="Legend Title",
    xaxis_title="Simulation time(s)",
    yaxis_title="Data rate(requests/s)",
    font=dict(
        size=20,
        # color="RebeccaPurple"
    )
)

y_range = [i for i in range(10, 15)]
fig.update_xaxes(range=[0, 300])
fig.update_yaxes(range=[0, 100], dtick=10)
fig.show()
fig.write_html("file.html")

