import telos
import argparse
import math
import tomllib
import datetime as dt
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path
from importlib.resources import files

def startup():

    case = {
        "airplanes": [
            Path(r"D:\Users\jgros\Documents\GitHub\atlas\src\telos\data\airplanes\c152.toml"), 
            Path(r"D:\Users\jgros\Documents\GitHub\atlas\src\telos\data\airplanes\aa5a.toml"),
            Path(r"D:\Users\jgros\Documents\GitHub\atlas\src\telos\data\airplanes\aa5b.toml")
        ]
    }

    columns = [
        "Airplane",
        "Mission",
        "Maximum BHP",
        "Maximum RPM",
        "Minimum RPM",
        "BSFC",
        "FF",
        "Time",
        "Fuel",
        "Distance",
    ]

    units = {
        "Airplane": "None",
        "Mission": "None",
        "Maximum BHP": "bhp",
        "Maximum RPM": "rpm",
        "Minimum RPM": "rpm",
        "BSFC": "lb/hp-hr",
        "FF": "gph",
        "Time": "hh:mm",
        "Fuel": "gal",
        "Distance": "nmi",
    }

    rows = [units]

    for i in case["airplanes"]:

        with open(i, "rb") as f:
            airplane = tomllib.load(f)

        name = airplane["name"]
        maximum_bhp = airplane["maximum_bhp"]["value"]
        maximum_rpm = airplane["maximum_rpm"]["value"]
        minimum_rpm = airplane["minimum_rpm"]["value"]
        bsfc = airplane["bsfc"]["value"]
        ff = bsfc * maximum_bhp * (minimum_rpm / maximum_rpm) * (1 / 6) # 1/6 converts PPH to GPH
        time = dt.timedelta(hours=0, minutes=15)
        fuel = ff * (time.total_seconds() / 3600) # second term converts time to hours
        dist = 0 # distance is inherently zero

        ff = round(ff, 1)
        fuel = round(fuel, 1)
        dist = round(dist, 0)

        data = {
            "Airplane": name,
            "Mission": "IYK-CHD (Std.)",
            "Maximum BHP": maximum_bhp,
            "Maximum RPM": maximum_rpm,
            "Minimum RPM": minimum_rpm,
            "BSFC": bsfc,
            "FF": ff,
            "Time": "00:15",
            "Fuel": fuel,
            "Distance": dist,
        }

        rows.append(data)

    df = pd.DataFrame(rows, columns=columns)

    return df

def climb():

    df = pd.DataFrame()

    return df

def cruise():

    df = pd.DataFrame()

    return df

def loiter():

    df = pd.DataFrame()

    return df

def reserve():

    df = pd.DataFrame()

    return df

def shutdown():

    df = pd.DataFrame()

    return df

def main():

    try:

        # Command line arguments.
        parser = argparse.ArgumentParser(description=f"{telos.__title__} {telos.__version__}", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
        parser.add_argument("-i", "--input", type=Path, required=True, help="specifies the input file")
        parser.add_argument("-o", "--output", type=Path, required=True, help="specifies the output Excel workbook (.xlsx)")
        # parser.add_argument("--case", type=Path, required=True, help="specifies the input case file (.toml)")

        args = parser.parse_args()

        # Open the case file.
        # with open(args.case, "rb") as f:
        #     case = tomllib.load(f)

        df_startup = startup()
        df_climb = climb()
        df_cruise = cruise()
        df_loiter = loiter()
        df_reserve = reserve()
        df_shutdown = shutdown()

        df_dict = {
            "Startup, Taxi, Run-Up": df_startup,
            "Climb": df_climb,
            "Cruise": df_cruise,
            "Loiter": df_loiter,
            "Reserve": df_reserve,
            "Taxi, Shutdown": df_shutdown,
        }

    except Exception as e:
        print(e)

    else:
        with pd.ExcelWriter(args.output, engine="openpyxl") as writer:
            for key, df in df_dict.items():
                df.to_excel(writer, sheet_name=key, index=False)

    finally:
        print("Complete!")

    # # Iterate over airplanes in the case file.
    # for i in case["airplanes"]:

    #     toml_file = files("telos.data.airplanes").joinpath(i).with_suffix(".toml")

    #     with toml_file.open("rb") as f:
    #         data = tomllib.load(f)

    #     print(data["name"])

    #     # Weight & balance
    #     bhp = data["brake_horsepower"]["value"]
    #     gross_weight = data["maximum_gross_weight"]["value"]

    #     # Takeoff distance

    #     print(data["takeoff_ground_roll_distance"]["coefficients"])

    #     # Climb
    #     model = data["rate_of_climb"]["model"]
    #     bsfc = 0.45 # 0.45 lb/bhp/hr per Raymer
    #     percent_bhp = 1.00

    #     df = pd.DataFrame()

    #     df["density_altitude"] = h

    #     for density_altitude in h:

    #         x = pd.Series(
    #             {
    #                 "constant": 0,
    #                 "gross_weight": gross_weight,
    #                 "density_altitude": density_altitude,
    #             }
    #         )
    #         b = pd.Series(data["rate_of_climb"]["coefficients"])

    #         df["rate_of_climb"] = x @ b # equivalent to y = x*b^T + err

    #         df["time_to_climb"] = (1/b["density_altitude"])*math.log10(df["rate_of_climb"] / (b["constant"] + b["gross_weight"]*x["gross_weight"]))

    #         df["pph"] = bsfc*bhp*percent_bhp
    #         df["ff"] = df["pph"] / 6
    #         df["v"] = data["vy"]["value"]

    #         df["fuel_to_climb"] = df["ff"] * df["time_to_climb"]

    #         df["distance_to_climb"] = df["v"] * df["time_to_climb"]

    #     plt.plot(df["fuel_to_climb"], df["density_altitude"])
    #     plt.show()

        

        # Cruise speed

        # Cruise range

        # Landing distance