# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import datetime

import numpy as np
import xarray as xr
from climetlab.decorators import parameters
from climetlab.utils import download_and_cache

from . import Meteonet

"""
rainfall_diff_quality-code
rainfall_mean_quality-code
reflectivity_new
reflectivity_old
"""


class Part:
    def __init__(self, url, domain, variable, year, month, part):
        self.domain = domain
        self.variable = variable
        self.year = year
        self.month = month
        self.part = part

        url = f"{url}/radar/{variable}_{domain}_{year}_{month:02d}.{part}.npz"

        path = download_and_cache(url)
        self.content = np.load(path, allow_pickle=True)

        self.dates = self.content["dates"]
        self.missing = self.content["miss_dates"]

    @property
    def data(self):
        return self.content["data"]

    def match(self, date):
        date_plus_1 = date + datetime.timedelta(days=1)
        for d in self.dates:
            if d >= date and d < date_plus_1:
                return True
        return False

    def filter_dates(self, date):
        date_plus_1 = date + datetime.timedelta(days=1)
        result = []
        for d in self.dates:
            if d >= date and d < date_plus_1:
                result.append(d)
        return result

    def __repr__(self):
        return f"Radar[{self.variable}_{self.domain}_{self.year}_{self.month:02d}.{self.part}.npz]"


class MeteonetRadar(Meteonet):
    """
    See https://github.com/meteofrance/meteonet
    """

    @parameters(date=("date-list",))
    def __init__(self, domain="NW", variable="rainfall", date=20160101):
        self.variable = variable

        parts = {}
        for d in date:
            yyyymm = d.strftime("%Y%m")
            for p in range(3):
                if (yyyymm, p) not in parts:
                    parts[(yyyymm, p)] = Part(
                        self.URL, domain, variable, d.year, d.month, p + 1
                    )

        url = "{url}/radar/radar_coords_{domain}.npz".format(
            url=self.URL, domain=domain
        )

        coords = np.load(download_and_cache(url), allow_pickle=True)

        resolution = 0.01

        lats = coords["lats"] - resolution / 2
        lons = coords["lons"] + resolution / 2

        use_parts = []
        for _, p in sorted(parts.items()):
            for d in date:
                if p.match(d):
                    use_parts.append(p)
                    break
        assert len(use_parts) == 1

        data = use_parts[0].data
        times = use_parts[0].dates

        ds = xr.Dataset(
            {
                variable: (["time", "y", "x"], data),
                "x": (["x"], range(0, data.shape[2])),
                "y": (["y"], range(0, data.shape[1])),
            },
            coords={
                "lon": (["y", "x"], lons),
                "lat": (["y", "x"], lats),
                "time": times,
            },
        )

        self.north = np.amax(lats)
        self.south = np.amin(lats)
        self.east = np.amax(lons)
        self.west = np.amin(lons)

        ds["lon"].attrs["standard_name"] = "longitude"
        ds["lat"].attrs["standard_name"] = "latitude"
        ds["time"].attrs["standard_name"] = "time"
        ds["x"].attrs["axis"] = "X"
        ds["y"].attrs["axis"] = "Y"

        dates = []
        for d in date:
            dates += use_parts[0].filter_dates(d)
        self._xarray = ds.sel(time=dates)

    def to_xarray(self):
        return self._xarray

    def plot_map(self, driver):
        driver.bounding_box(self.north, self.west, self.south, self.east)
        driver.plot_xarray(self._xarray, self.variable)
        driver.style("meteonet-radar-{}".format(self.variable))


dataset = MeteonetRadar
