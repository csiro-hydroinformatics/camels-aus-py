# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: fastai_pt
#     language: python
#     name: fai_pt
# ---

# %% [markdown]
# ## CAMELS-AUS
#
# **camels-aus** facilitates access from Python to the CAMELS-AUS dataset: [Fowler, K. J. A., Acharya, S. C., Addor, N., Chou, C., and Peel, M. C.: CAMELS-AUS: Hydrometeorological time series and landscape attributes for 222 catchments in Australia, Earth Syst. Sci. Data Discuss. [preprint], https://doi.org/10.5194/essd-2020-228, in review, 2021. ](https://essd.copernicus.org/preprints/essd-2020-228)
#

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
download_camels_aus(camels_dir)

# %%
repo.load_from_text_files(camels_dir)

# %%
repo.anthropogenicinfluences_attributes.copy()

# %%
import pandas as pd
time_interval = slice(pd.Timestamp('2009-01-01'), pd.Timestamp('2012-01-01')) 
repo.data.streamflow_mmd.sel(station_id='912101A', time=time_interval).plot(figsize = (16,4))

# %%
from camels_aus.read import load_csv_stations_metadata

# %%
repo.boundaries.plot()

# %% [markdown]
# ### Experimental interactive viewer with ipyleaflet
#
# Using personal experimental components ([ipyleaflet-dashboard-tools](https://github.com/jmp75/ipyleaflet-dashboard-tools)) that should probably find a home to [leafmaptools](https://github.com/giswqs/leafmaptools)
#
# ![leaflet_viewer_teaser.png](https://github.com/csiro-hydroinformatics/camels-aus-py/raw/testing/docs/examples/leaflet_viewer_teaser.png)
#

# %% [markdown]
# The following cells may work if you have installed ipleaflet and the experimental ipyleaflet tools. This is under constructions and not documented in details

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
