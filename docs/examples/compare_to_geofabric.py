# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: CAMELS
#     language: python
#     name: camels
# ---

# %%
import sys

# %%
sys.path

# %%
import camels_aus

# %%
import os
from camels_aus.repository import CamelsAus, download_camels_aus

# %% [markdown]
# `CamelsAus` is a repository that takes care of loading the data from disk and fives it access as a consolidated dataset to the user, using xarray for most data.

# %%
repo = CamelsAus()

# %% [markdown]
# `download_camels_aus` streamlines downloading and extracting the files making up CAMELS-AUS 1.0.

# %%
camels_dir = os.path.join(os.getenv("HOME"), 'data/camels/aus')

# %%
repo.load_from_text_files(camels_dir)
repo.data

# %%
import matplotlib
from ipywidgets import Output, HBox
from ipyleaflet_dashboard_tools.gv import *

import json
from ipyleaflet import Map, GeoJSON

# %%
# %%time 
ds = repo.data
v = GeoViewer(ds, lat='lat_outlet', lon='long_outlet', key='station_id')

out = Output()

click_handler_plot_ts = v.mk_click_handler_plot_ts(out, variable="streamflow_mmd")
mapview = v.build_map(click_handler_plot_ts)

mapview.layout.height = '600px'

# %%
# %%time 
gj = repo.boundaries.to_json()
d = json.loads(gj)

# %%
# %%time 
geo_json = GeoJSON(data=d, style = {'color': 'Blue', 'opacity':1, 'weight':1.9, 'dashArray':'9', 'fillOpacity':0.1})
mapview.add_layer(geo_json)

# %%
HBox([mapview, out])

# %%



# %%

# %%
import requests

# %%
loci_mdb = "https://gds.loci.cat/geometry/geofabric2_1_1_awradrainagedivision/9400206?_format=application/json&_view=simplifiedgeom"
def random_color(feature):
    return {
        'color': 'black',
        'fillColor': 'green',#random.choice(['red', 'yellow', 'green', 'orange']),
    }


# %%
mdb = json.loads(requests.get(loci_mdb).text)

# %%
geo_json_mdb = GeoJSON(
    data=mdb,
    style={
        'opacity': 1, 'dashArray': '9', 'fillOpacity': 0.1, 'weight': 1
    },
    hover_style={
        'color': 'green', 'dashArray': '0', 'fillOpacity': 0.3
    },
    style_callback=random_color
)

# %%
mapview.add_layer(geo_json_mdb)
# m.add_layer(bbox_poly)
# m.add_layer(geo_json_stations)

# %%
from sidecar import Sidecar

# %%
from IPython.display import display, clear_output, HTML, JSON

# %%
sc = Sidecar(title='MDB sites')
with sc:
    display(mapview)

# %%

# %%
get_cap = 'http://waterinfo1-cdc.it.csiro.au:8600/geoserver/wfs?service=wfs&version=2.0.0&request=GetCapabilities'

# %%
s = requests.get(get_cap).text

# %%
s

# %%
mdb = json.loads(requests.get(get_cap).text)

# %%
