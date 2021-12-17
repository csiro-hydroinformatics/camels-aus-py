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
    STATIONS_DIM_NAME,
    LEAD_TIME_DIM_NAME,
    TIME_DIM_NAME,
    ENSEMBLE_MEMBER_DIM_NAME,
    STR_LENGTH_DIM_NAME,
    STATION_ID_VARNAME,
    STATION_NAME_VARNAME,
    LAT_VARNAME,
    LON_VARNAME,
    X_VARNAME,
    Y_VARNAME,
    AREA_VARNAME,
    ELEVATION_VARNAME,
]

MANDATORY_GLOBAL_ATTRIBUTES = ["title", "institution", "source", "catchment", "comment"]


def get_default_dim_order():
    return [
        LEAD_TIME_DIM_NAME,
        STATIONS_DIM_NAME,
        ENSEMBLE_MEMBER_DIM_NAME,
        TIME_DIM_NAME,
    ]


def check_index_found(index_id, identifier: str, dimension_id: str):
    if index_id is None:
        raise ValueError(
            str.format(
                "identifier '{0}' not found in the dimension '{1}'",
                identifier,
                dimension_id,
            )
        )


def metadata_names():
    return [
        STATION_NAME_VARNAME,
        DRAINAGE_DIVISION_VARNAME,
        RIVER_REGION_VARNAME,
        NOTES_VARNAME,
    ]


def other_attributes_names():
    return [
        "pop_mean",
        "pop_max",
        "pop_gt_1",
        "pop_gt_10",
        "erosivity",
        "anngro_mega",
        "anngro_meso",
        "anngro_micro",
        "gromega_seas",
        "gromeso_seas",
        "gromicro_seas",
        "npp_ann",
        "npp_1",
        "npp_2",
        "npp_3",
        "npp_4",
        "npp_5",
        "npp_6",
        "npp_7",
        "npp_8",
        "npp_9",
        "npp_10",
        "npp_11",
        "npp_12",
    ]


def anthropogenicinfluences_attributes_names():
    return [
        "distupdamw",
        "impound_fac",
        "flow_div_fac",
        "leveebank_fac",
        "infrastruc_fac",
        "settlement_fac",
        "extract_ind_fac",
        "landuse_fac",
        "catchment_di",
        "flow_regime_di",
        "river_di",
    ]


def landcover_attributes_names():
    return [
        "lc01_extracti",
        "lc03_waterbo",
        "lc04_saltlak",
        "lc05_irrcrop",
        "lc06_irrpast",
        "lc07_irrsuga",
        "lc08_rfcropp",
        "lc09_rfpastu",
        "lc10_rfsugar",
        "lc11_wetlands",
        "lc14_tussclo",
        "lc15_alpineg",
        "lc16_openhum",
        "lc18_opentus",
        "lc19_shrbsca",
        "lc24_shrbden",
        "lc25_shrbope",
        "lc31_forclos",
        "lc32_foropen",
        "lc33_woodope",
        "lc34_woodspa",
        "lc35_urbanar",
        "prop_forested",
        "nvis_grasses_n",
        "nvis_grasses_e",
        "nvis_forests_n",
        "nvis_forests_e",
        "nvis_shrubs_n",
        "nvis_shrubs_e",
        "nvis_woodlands_n",
        "nvis_woodlands_e",
        "nvis_bare_n",
        "nvis_bare_e",
        "nvis_nodata_n",
        "nvis_nodata_e",
    ]


def topography_attributes_names():
    return [
        "elev_min",
        "elev_max",
        "elev_mean",
        "elev_range",
        "mean_slope_pct",
        "upsdist",
        "strdensity",
        "strahler",
        "elongratio",
        "relief",
        "reliefratio",
        "mrvbf_prop_0",
        "mrvbf_prop_1",
        "mrvbf_prop_2",
        "mrvbf_prop_3",
        "mrvbf_prop_4",
        "mrvbf_prop_5",
        "mrvbf_prop_6",
        "mrvbf_prop_7",
        "mrvbf_prop_8",
        "mrvbf_prop_9",
        "confinement",
    ]


def geology_attributes_names():
    return [
        "geol_prim",
        "geol_prim_prop",
        "geol_sec",
        "geol_sec_prop",
        "unconsoldted",
        "igneous",
        "silicsed",
        "carbnatesed",
        "othersed",
        "metamorph",
        "sedvolc",
        "oldrock",
        "claya",
        "clayb",
        "sanda",
        "solum_thickness",
        "ksat",
        "solpawhc",
    ]


def location_boundary_names():
    return [
        "lat_outlet",
        "long_outlet",
        "lat_centroid",
        "long_centroid",
        "map_zone",
        "catchment_area",
        "nested_status",
        "next_station_ds",
        "num_nested_within",
    ]


def streamflow_gaugingstats_names():
    return [
        "start_date",
        "end_date",
        "prop_missing_data",
        "q_uncert_num_curves",
        "q_uncert_n",
        "q_uncert_q10",
        "q_uncert_q10_upper",
        "q_uncert_q10_lower",
        "q_uncert_q50",
        "q_uncert_q50_upper",
        "q_uncert_q50_lower",
        "q_uncert_q90",
        "q_uncert_q90_upper",
        "q_uncert_q90_lower",
    ]


STREAMFLOW_MMD_VARNAME = "streamflow_mmd"
STREAMFLOW_QUALITYCODES_VARNAME = "streamflow_QualityCodes"
PRECIPITATION_AWAP_VARNAME = "precipitation_AWAP"
ET_MORTON_ACTUAL_SILO_VARNAME = "et_morton_actual_SILO"

SOLARRAD_AWAP_VARNAME = "solarrad_awap"
TMAX_AWAP_VARNAME = "tmax_awap"
TMIN_AWAP_VARNAME = "tmin_awap"
VPRP_AWAP_VARNAME = "vprp_awap"

XR_UNITS_ATTRIB_ID: str = "units"
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
        return ""
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


def check_camels_aus_version(version):
    if version != "1.0":
        raise ValueError(
            "camels-aus-py does not (yet) support version {version} of the CAMELS-AUS the dataset. Only version 1.0 of the data"
        )
