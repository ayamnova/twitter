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
# Append hover text
usize[0]['text'] = list(zip(df['State'], df['Users']))
sent = [ dict(
        type = 'choropleth',
        locations = df['Code'],
        locationmode='USA-states',
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
            title = 'Postiive State Tweets <br>Divided by Total Tweets')
      ) ]
# Append hover text
sent[0]['text'] = list(zip(df['State'], df['Sentiment']))

layout = go.Layout(
    geo = dict(
        resolution = 50,
        scope = 'usa',
        showframe = False,
        showcoastlines = True,
        showland = True,
        landcolor = "rgb(229, 229, 229)",
        countrycolor = "rgb(255, 255, 255)" ,
        coastlinecolor = "rgb(255, 255, 255)",
        projection = dict(
            type = 'albers usa'
            )
        )
    )

fig = go.Figure(layout=layout, data=usize + sent)
plotly.offline.plot(fig, filename='./out/smap.html')
