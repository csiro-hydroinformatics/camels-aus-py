import xarray as xr
import pandas as pd
import numpy as np

STATIONS_DIM_NAME = "station"
LEAD_TIME_DIM_NAME = "lead_time"
TIME_DIM_NAME = "time"
ENSEMBLE_MEMBER_DIM_NAME = "ens_member"
STR_LENGTH_DIM_NAME = "str_len"

# int station_id[station]   
STATION_ID_VARNAME = "station_id"
# char station_name[str_len,station]   
STATION_NAME_VARNAME = "station_name"
# float lat[station]   
LAT_VARNAME = "lat"
# float lon[station]   
LON_VARNAME = "lon"
# float x[station]   
X_VARNAME = "x"
# float y[station]   
Y_VARNAME = "y"
# float area[station]   
AREA_VARNAME = "area"
# float elevation[station]   
ELEVATION_VARNAME = "elevation"

DRAINAGE_DIVISION_VARNAME = "drainage_division"	
RIVER_REGION_VARNAME = "river_region"
NOTES_VARNAME = "notes"

CONVENTIONAL_VARNAMES = [
    STATIONS_DIM_NAME ,
    LEAD_TIME_DIM_NAME ,
    TIME_DIM_NAME ,
    ENSEMBLE_MEMBER_DIM_NAME ,
    STR_LENGTH_DIM_NAME ,
    STATION_ID_VARNAME ,
    STATION_NAME_VARNAME ,
    LAT_VARNAME ,
    LON_VARNAME ,
    X_VARNAME ,
    Y_VARNAME ,
    AREA_VARNAME ,
    ELEVATION_VARNAME
]

MANDATORY_GLOBAL_ATTRIBUTES = ["title", "institution", "source", "catchment", "comment"]

def get_default_dim_order():
    return [LEAD_TIME_DIM_NAME, STATIONS_DIM_NAME, ENSEMBLE_MEMBER_DIM_NAME, TIME_DIM_NAME]

def check_index_found(index_id, identifier, dimension_id):
    # return isinstance(index_id, np.int64)
    if index_id is None:
        raise Exception( str.format("identifier '{0}' not found in the dimension '{1}'", identifier, dimension_id))

XR_UNITS_ATTRIB_ID: str = 'units'
"""key for the units attribute on xarray DataArray objects"""


def set_xr_units(x: xr.DataArray, units: str):
    """Sets the units attribute of an xr.DataArray. No effect if x is not a dataarray

    Args:
        x (xr.DataArray): data array
        units (str): units descriptor
    """
    if units is None:
        return
    if isinstance(x, xr.DataArray):
        x.attrs[XR_UNITS_ATTRIB_ID] = units


def get_xr_units(x: xr.DataArray) -> str:
    """Gets the units attribute of an xr.DataArray. Empty string if no attribute

    Args:
        x (xr.DataArray): data array
    """
    assert isinstance(x, xr.DataArray)
    if not XR_UNITS_ATTRIB_ID in x.attrs.keys():
        return ''
    else:
        return x.attrs[XR_UNITS_ATTRIB_ID]


def copy_xr_units(src: xr.DataArray, target: xr.DataArray):
    """Copy the units attributes from one data array to another

    Args:
        src (xr.DataArray): source data array
        target (xr.DataArray): destination data array
    """
    if XR_UNITS_ATTRIB_ID in src.attrs.keys():
        target.attrs[XR_UNITS_ATTRIB_ID] = src.attrs[XR_UNITS_ATTRIB_ID]




