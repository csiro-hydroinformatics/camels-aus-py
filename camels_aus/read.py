from typing import Callable, Dict, List, Tuple
import pandas as pd
import numpy as np
import xarray as xr

from .conventions import *

def column_values(df:pd.DataFrame, colname:str) -> np.ndarray:
    return df[[colname]].values.transpose().squeeze()

timestamp_v = np.vectorize(pd.Timestamp)

import xarray as xr

def negative_is_missing(x:np.ndarray) -> np.ndarray:
    return x < 0.0

def load_csv_stations_tseries(filename:str, is_missing:Callable[[np.ndarray], np.ndarray]= None, units:str=None, dtype=None) -> xr.DataArray:
    """Loads a CAMELS-Aus time series from a comma-separated values file 

    Args:
        filename (str): filename
        is_missing (Callable[[np.ndarray], np.ndarray], optional): Function that post-processes the loaded time series to set missing values to np.nan (e.g. replace all negative values). Defaults to None, in which case nothing is changed.
        units (str, optional): Units of the time series. Defaults to None.
        dtype ([type], optional): expected column type. See pandas.read_csv. Defaults to None.

    Returns:
        xr.DataArray: A multivariate time series, xarray of dimension 2 (time X stations)
    """    
    if dtype is None:
        dtype = 'str'
    c_flows = pd.read_csv(filename, index_col=False, dtype=dtype)
    # TODO sanity checks
    indx = timestamp_v( year=column_values(c_flows, 'year').astype(np.int32),
        month=column_values(c_flows, 'month').astype(np.int32),
        day=column_values(c_flows, 'day').astype(np.int32))
    x = c_flows.drop(['year','month','day'], axis=1)
    x.index = pd.DatetimeIndex(indx)
    if not is_missing is None:
        missing = is_missing(x)
        x[missing] = np.nan
    res = xr.DataArray(x.values, 
                coords={TIME_DIM_NAME: pd.DatetimeIndex(indx), STATION_ID_VARNAME: x.columns}, 
                dims = [TIME_DIM_NAME, STATION_ID_VARNAME])
    set_xr_units(res, units)
    return res

def _mk_oned_var(dim_name, dim_values, var_values:np.ndarray):
    return xr.DataArray(var_values, 
                coords={dim_name: dim_values}, 
                dims = [dim_name])

def _all_in(names, a_set):
    return np.all([x in a_set for x in names])

def load_csv_stations_columns(filename:str, colnames:List[str]=None, station_id_varname=STATION_ID_VARNAME) -> Dict[str,np.ndarray]:
    x = pd.read_csv(filename)
    assert _all_in(colnames, x.columns)
    assert station_id_varname in x.columns
    station_ids = column_values(x, station_id_varname)
    y = [(colname, _mk_oned_var(station_id_varname, station_ids, column_values(x, colname))) for colname in colnames]
    return dict(y)

def load_csv_stations_metadata(filename:str) -> Dict[str,np.ndarray]:
    return load_csv_stations_columns(filename, 
        colnames= [STATION_NAME_VARNAME, DRAINAGE_DIVISION_VARNAME, RIVER_REGION_VARNAME, NOTES_VARNAME],
        station_id_varname=STATION_ID_VARNAME)


