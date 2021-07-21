import os
from camels_aus.variables import create_variable_definition
import numpy as np
from numpy.core.fromnumeric import shape
import pandas as pd
from datetime import datetime

pkg_dir = os.path.join(os.path.dirname(__file__),'..')
# sys.path.insert(0, pkg_dir)

from camels_aus.wrapper import *
from camels_aus.dimensions import *
from camels_aus.attributes import *

variable_names = ["variable_1", "variable_2"]
stations_ids = [123, 456]

nEns = 3
nLead = 4
x = np.arange(1, (nEns * nLead) + 1)
x = x.reshape((nLead, nEns))
y = x + nEns * nLead
import datetime

timeAxisStart = pd.Timestamp(year = 2010, month = 8, day = 1, hour = 12, minute = 0, 
  second = 0, tz= 'UTC')
tested_fcast_issue_time = timeAxisStart + pd.Timedelta(6,'h')
v1 = variable_names[0]
s1 = stations_ids[0]
v2 = variable_names[1]
s2 = stations_ids[1]


def dhours(i):
    return pd.Timedelta(i,'h')
def ddays(i):
    return pd.Timedelta(i * 24,'h')



def test_read_thing():
    fn = os.path.join(pkg_dir, 'tests','data','hourly_test.nc')
    assert os.path.exists(fn)
    ds = EftsDataSet(fn)
    assert set(ds.get_dim_names()) == set(['ens_member', 'lead_time', 'station', 'str_len', 'time'])
    r1 = ds.get_ensemble_forecasts(variable_name = v1, identifier = s1, start_time = tested_fcast_issue_time)
    r2 = ds.get_ensemble_forecasts(variable_name = v2, identifier = s2, start_time = tested_fcast_issue_time)
    assert r1[1,1] == 6
    assert r2[1,1] == 18
    # Check the lead time axix:
    # fcast_timeaxis = index(r1)
    # assert (fcast_timeaxis[0], tested_fcast_issue_time + lead_ts(lead_time_step_start_offset))
    # assert (fcast_timeaxis[1], tested_fcast_issue_time + lead_ts(lead_time_step_start_offset + lead_time_step_delta))

# put tests in a tryCatch, to maximise the chances of cleaning up temporary
# files.
def doTests(tempNcFname, lead_time_tstep = "hours", time_step = "hours since", time_step_delta = 1, lead_time_step_start_offset = 1, lead_time_step_delta = 1):

    # lead_time_tstep = "days"
    # time_step = "days since"
    # time_step_delta = 1L
    # lead_time_step_start_offset = 1L
    # lead_time_step_delta = 1L

    case_params = ''.join(["lts=", lead_time_tstep, ",ts=", time_step, ",tsdelta=", str(time_step_delta), ",ltsoffset=", str(lead_time_step_start_offset), ",ltsdelta=", str(lead_time_step_delta)])

    time_dim_info = create_time_info(start = timeAxisStart, n = 10, time_step = time_step, time_step_delta = time_step_delta)

    n = len(variable_names)
    varsDef = pd.DataFrame.from_dict(
        {
            'name' : variable_names,
            'longname' : ["long name for " + name for name in variable_names],
            'units' : np.repeat("mm", n),
            'missval' : np.repeat(-999, n),
            'precision' : np.repeat("double", n),
            'type' : np.repeat(2, n),
            'dimensions' : np.repeat("4", n),
            'type_description' : np.repeat("accumulated over the previous time step", n),
            'location_type' : np.repeat("Point", n),
        }    
    )
    glob_attr = create_global_attributes(title="title test", institution="test", source="test", catchment="dummy", comment="none")

    snc = create_efts(tempNcFname, time_dim_info, create_variable_definitions(varsDef), 
      stations_ids, nc_attributes=glob_attr, lead_length = nLead, ensemble_length = nEns, lead_time_tstep=lead_time_tstep)
    lead_times_offsets = np.arange(lead_time_step_start_offset, lead_time_step_start_offset+nLead) * lead_time_step_delta 

    snc.put_lead_time_values(lead_times_offsets)

    snc.put_ensemble_forecasts(x, variable_name = v1, identifier = s1, start_time = tested_fcast_issue_time)
    snc.put_ensemble_forecasts(y, variable_name = v2, identifier = s2, start_time = tested_fcast_issue_time)
    
    r1 = snc.get_ensemble_forecasts(variable_name = v1, identifier = s1, start_time = tested_fcast_issue_time)
    r2 = snc.get_ensemble_forecasts(variable_name = v2, identifier = s2, start_time = tested_fcast_issue_time)
    assert r1[1,1] == 6
    assert r2[1,1] == 18
    snc.write()

    if lead_time_tstep == "hours":
        lead_ts = dhours
    elif lead_time_tstep == "days":
        lead_ts = ddays
  
    snc = open_efts(tempNcFname)
    r1 = snc.get_ensemble_forecasts(variable_name = v1, identifier = s1, start_time = tested_fcast_issue_time)
    r2 = snc.get_ensemble_forecasts(variable_name = v2, identifier = s2, start_time = tested_fcast_issue_time)
    assert r1[1,1] == 6
    assert r2[1,1] == 18
    # Check the lead time axix:
    fcast_timeaxis = r1.lead_time
    assert fcast_timeaxis[0] == tested_fcast_issue_time + lead_ts(lead_time_step_start_offset)
    assert fcast_timeaxis[1] == tested_fcast_issue_time + lead_ts(lead_time_step_start_offset + lead_time_step_delta)
    snc.close()


import tempfile


def test_round_trip():

    with tempfile.TemporaryDirectory() as temp_dir:

        tested_fcast_issue_time = timeAxisStart + ddays(2)
        # Covers https://github.com/jmp75/efts/issues/6
        tempNcFname = os.path.join(temp_dir, 'days.nc')
        doTests(tempNcFname, lead_time_tstep = "days", time_step = "days since", time_step_delta = 1, lead_time_step_start_offset = 1, lead_time_step_delta = 1)

        tested_fcast_issue_time = timeAxisStart + dhours(6)

        tempNcFname = os.path.join(temp_dir, 'hourly.nc')
        doTests(tempNcFname, lead_time_tstep = "hours", time_step = "hours since", time_step_delta = 1, lead_time_step_start_offset = 1, lead_time_step_delta = 1)

        tempNcFname = os.path.join(temp_dir, 'three_hourly.nc')
        doTests(tempNcFname, lead_time_tstep = "hours", time_step = "hours since", time_step_delta = 1, lead_time_step_start_offset = 1, lead_time_step_delta = 3)

if __name__ == "__main__":
    test_read_thing()
    test_round_trip()
