from typing import Callable, Dict, List
import pandas as pd
import numpy as np
import xarray as xr
import os

from .conventions import *
from .read import *

class CamelsAus:

    def __init__(self, subset:List[str]=None, timespan=None) -> None:
        pass

    def load_from_text_files(self, directory:str, version:str='1.0') -> None:
        # directory = '/home/per202/data/camels/aus'
        id_name_metadata_fn = os.path.join(directory, '01_id_name_metadata/id_name_metadata.csv')
        self._id_name_metadata = load_csv_stations_metadata(id_name_metadata_fn)

        location_boundary_area_dir = os.path.join(directory, '02_location_boundary_area')
        location_boundary_area_fn = os.path.join(location_boundary_area_dir, 'location_boundary_area.csv')

        location_boundary_colnames = ["lat_outlet","long_outlet","lat_centroid","long_centroid","map_zone","catchment_area","nested_status","next_station_ds","num_nested_within"]
        self._location_boundary_area = load_csv_stations_columns(location_boundary_area_fn, colnames = location_boundary_colnames)

        # streamflow_mmd.csv
        streamflow_dir = os.path.join(directory, '03_streamflow')
        streamflow_fn = os.path.join(streamflow_dir, 'streamflow_mmd.csv')
        self._streamflow_mmd = load_csv_stations(streamflow_fn, is_missing=negative_is_missing, units='mm')

        # streamflow_GaugingStats.csv
        streamflow_GaugingStats_fn = os.path.join(streamflow_dir, 'streamflow_GaugingStats.csv')
        streamflow_GaugingStats_colnames = ["start_date","end_date","prop_missing_data",
            "q_uncert_num_curves","q_uncert_n","q_uncert_q10","q_uncert_q10_upper",
            "q_uncert_q10_lower","q_uncert_q50","q_uncert_q50_upper","q_uncert_q50_lower",
            "q_uncert_q90","q_uncert_q90_upper","q_uncert_q90_lower"]

        self._streamflow_GaugingStats = load_csv_stations_columns(streamflow_GaugingStats_fn, colnames = streamflow_GaugingStats_colnames)
        # streamflow_MLd.csv
        # streamflow_MLd_inclInfilled.csv
        # streamflow_QualityCodes.csv
        # streamflow_signatures.csv

        d = dict(self._id_name_metadata)
        d.update(self._location_boundary_area)
        d.update({'streamflow_mmd': self._streamflow_mmd})
        self._ds = xr.Dataset( data_vars = d )

    @property
    def data(self) -> xr.Dataset:
        """ Camels aggregated xarray dataset  """
        return self._ds

    def load_from_cached_files(self, directory:str, version:str='1.0') -> None:
        pass

    def save_to_cached_files(self, directory:str, version:str='1.0') -> None:
        pass
