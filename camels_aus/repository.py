"""Access arrangements to the CAMELS-AUS dataset
"""

from typing import List
import numpy as np
import xarray as xr
import os
import geopandas as gpd

from .conventions import (check_camels_aus_version, 
    other_attributes_names,
    anthropogenicinfluences_attributes_names,
    landcover_attributes_names,
    topography_attributes_names,
    geology_attributes_names,
)
from .read import (load_csv_stations_columns, load_csv_stations_metadata, load_csv_stations_tseries, load_streamflow_gaugingstats, negative_is_missing,
    load_boundary_area,
    load_geology_attributes,
    load_topography_attributes,
    load_landcover_attributes,
    load_anthropogenicinfluences_attributes,
    load_other_attributes,
    STREAMFLOW_MMD_VARNAME,
    STREAMFLOW_QUALITYCODES_VARNAME,
    PRECIPITATION_AWAP_VARNAME,
    ET_MORTON_ACTUAL_SILO_VARNAME,
)


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
    check_camels_aus_version(version)
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

    check_camels_aus_version(version)

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
        check_camels_aus_version(version)
        if not os.path.exists(directory):
            raise FileNotFoundError("Directory {0} not found".format(directory))
        id_name_metadata_dir = os.path.join(directory, '01_id_name_metadata')
        id_name_metadata_fn = os.path.join(id_name_metadata_dir, 'id_name_metadata.csv')
        _check_fileexists(id_name_metadata_fn)
        _id_name_metadata = load_csv_stations_metadata(id_name_metadata_fn)

        location_boundary_area_dir = os.path.join(directory, '02_location_boundary_area')
        location_boundary_area_fn = os.path.join(location_boundary_area_dir, 'location_boundary_area.csv')
        _check_fileexists(location_boundary_area_fn)
        _location_boundary_area = load_boundary_area(location_boundary_area_fn)

        attributes_dir = os.path.join(directory, '04_attributes')
        catchmentattributes_01_geology_fn = os.path.join(attributes_dir, 'CatchmentAttributes_01_Geology&Soils.csv')
        catchmentattributes_02_topography_fn = os.path.join(attributes_dir, 'CatchmentAttributes_02_Topography&Geometry.csv')
        catchmentattributes_03_landcover_fn = os.path.join(attributes_dir, 'CatchmentAttributes_03_LandCover&Vegetation.csv')
        catchmentattributes_04_anthropogenicinfluences_fn = os.path.join(attributes_dir, 'CatchmentAttributes_04_AnthropogenicInfluences.csv')
        catchmentattributes_05_other_fn = os.path.join(attributes_dir, 'CatchmentAttributes_05_Other.csv')
        # 'Landcover_timeseries.xlsx'
        _check_fileexists(catchmentattributes_01_geology_fn)
        _check_fileexists(catchmentattributes_02_topography_fn)
        _check_fileexists(catchmentattributes_03_landcover_fn)
        _check_fileexists(catchmentattributes_04_anthropogenicinfluences_fn)
        _check_fileexists(catchmentattributes_05_other_fn)
        
        _geology_attributes = load_geology_attributes(catchmentattributes_01_geology_fn)
        _topography_attributes = load_topography_attributes(catchmentattributes_02_topography_fn)
        _landcover_attributes = load_landcover_attributes(catchmentattributes_03_landcover_fn)
        _anthropogenicinfluences_attributes = load_anthropogenicinfluences_attributes(catchmentattributes_04_anthropogenicinfluences_fn)
        _other_attributes = load_other_attributes(catchmentattributes_05_other_fn)

        # streamflow_mmd.csv
        streamflow_dir = os.path.join(directory, '03_streamflow')
        streamflow_fn = os.path.join(streamflow_dir, 'streamflow_mmd.csv')
        _check_fileexists(streamflow_fn)
        _streamflow_mmd = load_csv_stations_tseries(streamflow_fn, is_missing=negative_is_missing, units='mm', dtype=np.float32)

        # streamflow_GaugingStats.csv
        streamflow_gauging_stats_fn = os.path.join(streamflow_dir, 'streamflow_GaugingStats.csv')
        _check_fileexists(streamflow_gauging_stats_fn)
        _streamflow_gauging_stats = load_streamflow_gaugingstats(streamflow_gauging_stats_fn)

        # streamflow_MLd.csv
        # streamflow_MLd_inclInfilled.csv
        # streamflow_QualityCodes.csv
        streamflow_quality_codes_fn = os.path.join(streamflow_dir, 'streamflow_QualityCodes.csv')
        _check_fileexists(streamflow_quality_codes_fn)
        streamflow_quality_codes = load_csv_stations_tseries(streamflow_quality_codes_fn, dtype='str')
        # streamflow_signatures.csv

        hydrometeorology_dir = os.path.join(directory, '05_hydrometeorology')
        
        precipitation_timeseries_dir = os.path.join(hydrometeorology_dir, '01_precipitation_timeseries')
        precipitation_awap_fn = os.path.join(precipitation_timeseries_dir, 'precipitation_AWAP.csv')
        _check_fileexists(precipitation_awap_fn)
        precipitation_awap = load_csv_stations_tseries(precipitation_awap_fn, is_missing=negative_is_missing, units='mm', dtype=np.float32)

        evap_timeseries_dir = os.path.join(hydrometeorology_dir, '02_EvaporativeDemand_timeseries')
        et_morton_actual_silo_fn = os.path.join(evap_timeseries_dir, 'et_morton_actual_SILO.csv')
        _check_fileexists(et_morton_actual_silo_fn)
        et_morton_actual_silo = load_csv_stations_tseries(et_morton_actual_silo_fn, is_missing=negative_is_missing, units='mm', dtype=np.float32)

        d = dict(_id_name_metadata)
        d.update({STREAMFLOW_MMD_VARNAME : _streamflow_mmd})
        d.update({STREAMFLOW_QUALITYCODES_VARNAME : streamflow_quality_codes})
        d.update({PRECIPITATION_AWAP_VARNAME : precipitation_awap})
        d.update({ET_MORTON_ACTUAL_SILO_VARNAME : et_morton_actual_silo})

        d.update(_streamflow_gauging_stats)
        d.update(_location_boundary_area)
        d.update(_geology_attributes)
        d.update(_topography_attributes)
        d.update(_landcover_attributes)
        d.update(_anthropogenicinfluences_attributes)
        d.update(_other_attributes)

        self._ds = xr.Dataset( data_vars = d )

        spatial_dir = os.path.join(directory, '02_location_boundary_area')
        boundaries_fn = os.path.join(spatial_dir, 'shp','CAMELS_AUS_Boundaries_adopted.shp')
        _check_fileexists(boundaries_fn)
        self.boundaries = gpd.read_file(filename=boundaries_fn)

    @property
    def data(self) -> xr.Dataset:
        """ Camels aggregated xarray dataset  """
        return self._ds

    @property
    def daily_data(self) -> xr.DataArray:
        """ All daily time series in the dataset """
        return self._ds[[STREAMFLOW_MMD_VARNAME,
            STREAMFLOW_QUALITYCODES_VARNAME,
            PRECIPITATION_AWAP_VARNAME,
            ET_MORTON_ACTUAL_SILO_VARNAME,
            ]]

    @property 
    def other_attributes(self) -> xr.DataArray: 
        return self._ds[other_attributes_names()]

    @property 
    def anthropogenicinfluences_attributes(self) -> xr.DataArray: 
        return self._ds[anthropogenicinfluences_attributes_names()]

    @property 
    def landcover_attributes(self) -> xr.DataArray: 
        return self._ds[landcover_attributes_names()]

    @property 
    def topography_attributes(self) -> xr.DataArray: 
        return self._ds[topography_attributes_names()]

    @property 
    def geology_attributes(self) -> xr.DataArray: 
        return self._ds[geology_attributes_names()]

    def load_from_cached_files(self, directory:str, version:str='1.0') -> None:
        raise NotImplemented("Not yet implemented")

    def save_to_cached_files(self, directory:str, version:str='1.0') -> None:
        raise NotImplemented("Not yet implemented")

