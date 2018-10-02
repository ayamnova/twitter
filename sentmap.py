import plotly.plotly as py
import plotly
import sys
import pandas as pd
from os.path import join as jn
from config import OUT, PROC

df = pd.read_csv(jn(OUT, sys.argv[1]))

data = [ dict(
        type = 'choropleth',
        locations = df['Code'],
        z = df['Sentiment'],
        text = df['Country'],
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

layout = dict(
    title = 'Sentimentality of Tweets Globally',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
plotly.offline.plot(fig, filename='./out/sentmap.html')
