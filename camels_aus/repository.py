"""Access arrangements to the CAMELS-AUS dataset
"""

from typing import List
import numpy as np
import xarray as xr
import os
import geopandas as gpd

from .conventions import *
from .read import *


def download_camels_aus(local_directory:str, version='1.0') -> None:
    """Long-running operation; download version 1.0 of the CAMELS-AUS dataset from the repository chosen by the authors.

    Args:
        local_directory (str): local directory where data will be downloaded and unzipped
        version (str, optional): version of the dataset. Defaults to '1.0' (only one supported currently).

    Raises:
        Exception: Incorrect version number. 
    """    
    import requests
    from zipfile import ZipFile
    os.makedirs(local_directory, exist_ok=True)
    if version != '1.0':
        raise Exception("Only version 1.0 is available as of 2021-03")
    zipfiles = [
        "01_id_name_metadata.zip",
        "02_location_boundary_area.zip",
        "03_streamflow.zip",
        "04_attributes.zip",
        "05_hydrometeorology.zip"
    ]
    other_files = [
        "CAMELS_AUS_Attributes-Indices_MasterTable.csv",
        "CAMELS_AUS_ReferenceList.pdf",
        "Units_01_TimeseriesData.pdf",
        "Units_02_AttributeMasterTable.pdf"
    ]
    all_files = zipfiles + other_files
    url_root = "https://download.pangaea.de/dataset/921850/files/"
    # URL of the image to be downloaded is defined as image_url 
    for fn in all_files:
        local_fn = os.path.join(local_directory, fn)
        if os.path.exists(local_fn):
            print("INFO: {0} already exists, skipping download".format(local_fn))
        else:
            fn_url = url_root + fn
            r = requests.get(fn_url) # create HTTP response object 
            print("INFO: Dowloading {0} ...".format(fn_url), flush=True)
            with open(local_fn,'wb') as f:         
                f.write(r.content) 
            print("INFO: Dowloaded {0}".format(fn_url))

    for fn in zipfiles:
        local_fn = os.path.join(local_directory, fn)
        expected_dir = os.path.splitext(local_fn)[0]
        if os.path.exists(expected_dir):
            print("INFO: {0} already exists, skipping extraction".format(expected_dir))
        else:
            print("INFO: Extracting {0} ...".format(local_fn), flush=True)
            with ZipFile(local_fn, 'r') as zipObj:
                zipObj.extractall(path=local_directory)
            print("INFO: Extracted {0}".format(local_fn))

    if version != '1.0':
        raise Exception("Only version 1.0 is available as of 2021-03")

def _check_fileexists(fn):
    if not os.path.exists(fn):
        raise FileNotFoundError("File {0} not found".format(fn))

class CamelsAus:
    """A facade to the CAMELS-AUS dataset to reduce the tedium in loading data
    """

    def __init__(self, subset:List[str]=None, timespan=None) -> None:
        """Constructor

        Args:
            subset (List[str], optional): IGNORED. Defaults to None.
            timespan ([type], optional): IGNORED. Defaults to None.
        """
        pass

    def load_from_text_files(self, directory:str, version:str='1.0') -> None:
        """Loads the CAMELS-AUS data from the reference form (mostly CSV files) into memory

        Args:
            directory (str): directory where the file-based data was downloaded and extracted.
            version (str, optional): version of the dataset. Defaults to '1.0' (only one supported currently).

        Raises:
            FileNotFoundError: One of the files in the dataset is not found
            Exception: Unhandled version
        """
        if version != '1.0':
            raise Exception("Only version 1.0 is available as of 2021-03")
        if not os.path.exists(directory):
            raise FileNotFoundError("Directory {0} not found".format(directory))
        id_name_metadata_dir = os.path.join(directory, '01_id_name_metadata')
        id_name_metadata_fn = os.path.join(id_name_metadata_dir, 'id_name_metadata.csv')
        _check_fileexists(id_name_metadata_fn)
        _id_name_metadata = load_csv_stations_metadata(id_name_metadata_fn)

        location_boundary_area_dir = os.path.join(directory, '02_location_boundary_area')
        location_boundary_area_fn = os.path.join(location_boundary_area_dir, 'location_boundary_area.csv')
        _check_fileexists(location_boundary_area_fn)

        location_boundary_colnames = ["lat_outlet","long_outlet","lat_centroid","long_centroid","map_zone","catchment_area","nested_status","next_station_ds","num_nested_within"]
        _location_boundary_area = load_csv_stations_columns(location_boundary_area_fn, colnames = location_boundary_colnames)

        # streamflow_mmd.csv
        streamflow_dir = os.path.join(directory, '03_streamflow')
        streamflow_fn = os.path.join(streamflow_dir, 'streamflow_mmd.csv')
        _check_fileexists(streamflow_fn)
        _streamflow_mmd = load_csv_stations_tseries(streamflow_fn, is_missing=negative_is_missing, units='mm', dtype=np.float32)

        # streamflow_GaugingStats.csv
        streamflow_GaugingStats_fn = os.path.join(streamflow_dir, 'streamflow_GaugingStats.csv')
        _check_fileexists(streamflow_GaugingStats_fn)
        streamflow_GaugingStats_colnames = ["start_date","end_date","prop_missing_data",
            "q_uncert_num_curves","q_uncert_n","q_uncert_q10","q_uncert_q10_upper",
            "q_uncert_q10_lower","q_uncert_q50","q_uncert_q50_upper","q_uncert_q50_lower",
            "q_uncert_q90","q_uncert_q90_upper","q_uncert_q90_lower"]
        _streamflow_GaugingStats = load_csv_stations_columns(streamflow_GaugingStats_fn, colnames = streamflow_GaugingStats_colnames)

        # streamflow_MLd.csv
        # streamflow_MLd_inclInfilled.csv
        # streamflow_QualityCodes.csv
        streamflow_QualityCodes_fn = os.path.join(streamflow_dir, 'streamflow_QualityCodes.csv')
        _check_fileexists(streamflow_QualityCodes_fn)
        streamflow_QualityCodes = load_csv_stations_tseries(streamflow_QualityCodes_fn, dtype='str')
        # streamflow_signatures.csv

        hydrometeorology_dir = os.path.join(directory, '05_hydrometeorology')
        
        precipitation_timeseries_dir = os.path.join(hydrometeorology_dir, '01_precipitation_timeseries')
        precipitation_AWAP_fn = os.path.join(precipitation_timeseries_dir, 'precipitation_AWAP.csv')
        _check_fileexists(precipitation_AWAP_fn)
        precipitation_AWAP = load_csv_stations_tseries(precipitation_AWAP_fn, is_missing=negative_is_missing, units='mm', dtype=np.float32)

        evap_timeseries_dir = os.path.join(hydrometeorology_dir, '02_EvaporativeDemand_timeseries')
        et_morton_actual_SILO_fn = os.path.join(evap_timeseries_dir, 'et_morton_actual_SILO.csv')
        _check_fileexists(et_morton_actual_SILO_fn)
        et_morton_actual_SILO = load_csv_stations_tseries(et_morton_actual_SILO_fn, is_missing=negative_is_missing, units='mm', dtype=np.float32)

        d = dict(_id_name_metadata)
        d.update({'streamflow_mmd': _streamflow_mmd})
        d.update({'streamflow_QualityCodes': streamflow_QualityCodes})
        d.update({'precipitation_AWAP': precipitation_AWAP})
        d.update({'et_morton_actual_SILO': et_morton_actual_SILO})
        d.update(_location_boundary_area)

        self._ds = xr.Dataset( data_vars = d )

        spatial_dir = os.path.join(directory, '02_location_boundary_area')
        boundaries_fn = os.path.join(spatial_dir, 'shp','CAMELS_AUS_Boundaries_adopted.shp')
        _check_fileexists(boundaries_fn)
        self.boundaries = gpd.read_file(filename=boundaries_fn)

    @property
    def data(self) -> xr.Dataset:
        """ Camels aggregated xarray dataset  """
        return self._ds

    def load_from_cached_files(self, directory:str, version:str='1.0') -> None:
        raise NotImplemented("Not yet implemented")

    def save_to_cached_files(self, directory:str, version:str='1.0') -> None:
        raise NotImplemented("Not yet implemented")
