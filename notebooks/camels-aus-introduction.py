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
#     display_name: Py3 WAA
#     language: python
#     name: waa
# ---

# %% [markdown]
# ## CAMELS-AUS
#
# [Fowler, K. J. A., Acharya, S. C., Addor, N., Chou, C., and Peel, M. C.: CAMELS-AUS: Hydrometeorological time series and landscape attributes for 222 catchments in Australia, Earth Syst. Sci. Data Discuss. [preprint], https://doi.org/10.5194/essd-2020-228, in review, 2021. ](https://essd.copernicus.org/preprints/essd-2020-228)
#
#

# %%
import os
from camels_aus.repository import CamelsAus, download_camels_aus

# %%
repo = CamelsAus()

# %%
camels_dir = os.path.join(os.getenv("HOME"), 'data/camels/aus')

# %%
download_camels_aus(camels_dir)

# %%
repo.load_from_text_files(camels_dir)
repo.data

# %%
import matplotlib
from ipywidgets import Output, HBox
from ipyleaflet_dashboard_tools.gv import *

# %%
v = GeoViewer(ds, lat='lat_outlet', lon='long_outlet', key='station_id')

# %%
out = Output()

# %%
click_handler_plot_ts = v.mk_click_handler_plot_ts(out, variable="streamflow_mmd")
mapview = v.build_map(click_handler_plot_ts)

mapview.layout.height = '600px'

# %%
HBox([mapview, out])

# %%
