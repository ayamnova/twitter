import plotly
import plotly.graph_objs as go

'''
plotly.offline.plot({
    "data": [go.Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": go.Layout(title="hello world")
    })
'''

trace1=go.Scatter(
        x = [1,2], y = [1,2])


trace2 = go.Scatter(
        x = [1,2], y = [2, 1])


plotly.offline.plot(
    [trace1, trace2]
    )
