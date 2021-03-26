# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


from climetlab import load_source
from climetlab.decorators import parameters

from . import Meteonet

PATTERN = (
    "{URL}"
    "/weather_models"
    "/{domain}_weather_models_{n}D_parameters_{date:date(%Y)}"
    "/{date:date(%Y%m)}"
    "/{model_upper}"
    "/{variable}"
    "/{model_lower}_{variable}_{domain}_{date:date(%Y%m%d)}{time}00.grib"
)

N_DIMENSIONS = {
    "2m": 2,
    "P_sea_level": 2,
    "10m": 2,
    "PRECIP": 2,
    "3D_height": 3,
    "3D_isobar": 3,
}


class MeteonetWeatherModels(Meteonet):
    """
    See https://github.com/meteofrance/meteonet
    """

    @parameters(date=("date-list",))
    def __init__(
        self, model="arome", variable="2m", domain="NW", date="20180501", time="0000"
    ):

        request = dict(
            URL=self.URL,
            domain=domain,
            variable=variable,
            date=date,
            time=time,
            model_upper=model.upper(),
            model_lower=model.lower(),
            n=N_DIMENSIONS[variable],
        )
        self.source = load_source("url-pattern", PATTERN, request)


dataset = MeteonetWeatherModels
