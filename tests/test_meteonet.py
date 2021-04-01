import climetlab as cml

DOMAINS = ("NW", "SE")
VARIABLES = (
    "2m",
    "P_sea_level",
    "10m",
    "PRECIP",
    "3D_height",
    "3D_isobar",
)

MODELS = ("arpege", "arome")


def test_radar():
    cml.load_dataset("meteonet-radar", date=[20180501])


def test_masks():
    for domain in DOMAINS:
        ds = cml.load_dataset("meteonet-masks", domain=domain)
        assert len(ds) == 2
        cml.plot_map(ds[0])
        cml.plot_map(ds[1])
        x = ds.to_xarray()
        cml.plot_map(x.lsm)
        cml.plot_map(x.p3008)


def test_weather_models():
    for domain in DOMAINS:
        for variable in VARIABLES:
            for model in MODELS:
                if model == "arome" and variable.startswith("3D"):
                    continue
                cml.load_dataset(
                    "meteonet-weather-models",
                    date=[20180601],
                    variable=variable,
                    model=model,
                    domain=domain,
                )
        # ds = cml.load_dataset("meteonet-weather-models", date=[20180501])
        # print(ds[0].path)
        # assert len(ds) == 2
        # print(ds.to_xarray())


def test_ground_stations():
    pass


if __name__ == "__main__":
    test_radar()
