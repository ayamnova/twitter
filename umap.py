import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import sys
import pandas as pd
from os.path import join as jn
from constants import OUT, PROC

df = pd.read_csv(jn(OUT, sys.argv[1]))
df.head()

usize = [go.Scattergeo(
        lon=df['Lon'],
        lat=df['Lat'],
        text=[],
        name="Number of Users",
        hoverinfo='text',
        marker=dict(
            size=df['Users']/1000,
            line=dict(width=0)
            )
        )]
usize[0]['text'] = list(zip(df['Country'], df['Users']))
sent = [ dict(
        type = 'choropleth',
        locations = df['Code'],
        z = df['Sentiment'],
        text = [],
        name="Sentiment",
        hoverinfo='text',
        colorscale = 'Viridis',
        reversescale = True,
        autocolorscale = False,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            title = 'Postiive Country Tweets <br>Divided by Total Tweets')
      ) ]
sent[0]['text'] = list(zip(df['Country'], df['Sentiment']))


'''
for i in range(6,10)[::-1]:
    cases.append(go.Scattergeo(
        lon = df[ df['Month'] == i ]['Lon'], #-(max(range(6,10))-i),
        lat = df[ df['Month'] == i ]['Lat'],
        text = df[ df['Month'] == i ]['Value'],
        name = months[i],
        marker = dict(
            size = df[ df['Month'] == i ]['Value']/50,
            color = colors[i-6],
            line = dict(width = 0)
        ),
    ) )
cases[0]['text'] = df[ df['Month'] == 9 ]['Value'].map('{:.0f}'.format).astype(str)+' '+\
    df[ df['Month'] == 9 ]['Country']
cases[0]['mode'] = 'markers+text'
cases[0]['textposition'] = 'bottom center'

inset = [
    go.Choropleth(
        locationmode = 'country names',
        locations = df[ df['Month'] == 9 ]['Country'],
        z = df[ df['Month'] == 9 ]['Value'],
        text = df[ df['Month'] == 9 ]['Country'],
        colorscale = [[0,'rgb(0, 0, 0)'],[1,'rgb(0, 0, 0)']],
        autocolorscale = False,
        showscale = False,
        geo = 'geo2'
    ),
    go.Scattergeo(
        lon = [21.0936],
        lat = [7.1881],
        text = ['Africa'],
        mode = 'text',
        showlegend = False,
        geo = 'geo2'
    )
]
'''

layout = go.Layout(
    geo = dict(
        resolution = 50,
        scope = 'world',
        showframe = False,
        showcoastlines = True,
        showland = True,
        landcolor = "rgb(229, 229, 229)",
        countrycolor = "rgb(255, 255, 255)" ,
        coastlinecolor = "rgb(255, 255, 255)",
        projection = dict(
            type = 'Mercator'
            )
        )
    )

fig = go.Figure(layout=layout, data=usize + sent)
plotly.offline.plot(fig, filename='./out/umap.html')
