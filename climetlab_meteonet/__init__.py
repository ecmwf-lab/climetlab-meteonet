# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

__version__ = "0.0.21"

from climetlab import Dataset



class Meteonet(Dataset):

    # FIXME: This is a temporary URL, for development only
    URL = "http://datastore.copernicus-climate.eu/meteonet/dataset/data/"

    home_page = "https://meteonet.umr-cnrm.fr"

    licence = "https://meteonet.umr-cnrm.fr/dataset/LICENCE.md"

    documentation = "https://meteofrance.github.io/meteonet/"

    DOMAINS = ["NW", "SE"]
    MODELS = ['arome', 'arpege']
