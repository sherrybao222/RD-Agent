import qlib

qlib.init(provider_uri="~/.qlib/qlib_data/cn_data")

from qlib.data import D

instruments = D.instruments()
fields = ["$open", "$close", "$high", "$low", "$volume", "$factor"]

# Full dataset
data = (
    D.features(instruments, fields, freq="day")
    .swaplevel()
    .sort_index()
    .loc["2008-12-29":]
    .sort_index()
)

data.to_hdf("./daily_pv_all.h5", key="data")

# Debug dataset: first choose instruments that actually have data
# during the requested debug period.
debug_raw = D.features(
    instruments,
    fields,
    start_time="2018-01-01",
    end_time="2019-12-31",
    freq="day",
).sort_index()

available_instruments = (
    debug_raw.index.get_level_values("instrument")
    .unique()
    .tolist()
)

selected_instruments = available_instruments[:100]

debug_data = (
    debug_raw.loc[selected_instruments]
    .swaplevel()
    .sort_index()
)

debug_data.to_hdf("./daily_pv_debug.h5", key="data")