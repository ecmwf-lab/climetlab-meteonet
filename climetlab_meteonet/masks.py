# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


from climetlab import load_source
from climetlab.normalize import normalize_args

from . import Meteonet


class MeteonetMasks(Meteonet):
    """
    See https://github.com/meteofrance/meteonet
    """

    @normalize_args(domain=Meteonet.DOMAINS)
    def __init__(
        self,
        domain="NW",
    ):

        url = "{url}/masks/{domain}_masks.grib".format(
            url=self.URL,
            domain=domain,
        )
        self.source = load_source("url", url, styles=["land-sea-mask", "orography"])


dataset = MeteonetMasks
