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

def startup(args: argparse.Namespace):

    case = {
        "airplanes": [
            Path(r"D:\Users\jgros\Documents\Github\atlas\src\telos\data\airplanes\c150m.toml"),
            Path(r"D:\Users\jgros\Documents\GitHub\atlas\src\telos\data\airplanes\c152.toml"), 
            Path(r"D:\Users\jgros\Documents\GitHub\atlas\src\telos\data\airplanes\aa5a.toml"),
            Path(r"D:\Users\jgros\Documents\GitHub\atlas\src\telos\data\airplanes\aa5b.toml"),
        ]
    }

    header = {
        "Airplane": "None",
        "Mission": "None",
        "Maximum BHP": "bhp",
        "Maximum RPM": "rpm",
        "Minimum RPM": "rpm",
        "BSFC": "lb/hp-hr",
        "%BHP": "percent",
        "FF": "gph",
        "TAS": "knots",
        "Time": "hh:mm",
        "Fuel": "gal",
        "Distance": "nmi",
    }

    rows = [header]

    for i in case["airplanes"]:

        with open(i, "rb") as f:
            airplane = tomllib.load(f)

        name = airplane["name"]
        maximum_bhp = airplane["maximum_bhp"]["value"]
        maximum_rpm = airplane["maximum_rpm"]["value"]
        minimum_rpm = airplane["minimum_rpm"]["value"]
        bsfc = airplane["bsfc"]["value"]
        percent_bhp = minimum_rpm / maximum_rpm

        # Segment fuel flow and true airspeed
        ff = bsfc * maximum_bhp * percent_bhp * (1 / 6) # 1/6 converts PPH to GPH
        tas = 0

        # Segment time, fuel, and distance
        time = dt.timedelta(hours=0, minutes=15)
        fuel = ff * (time.total_seconds() / 3600) # second term converts time to hours
        dist = tas * (time.total_seconds() / 3600)

        percent_bhp = round(percent_bhp*100, 0)
        ff = round(ff, 1)
        fuel = round(fuel, 1)
        dist = round(dist, 0)

        # Organize the data
        data = {
            "Airplane": name,
            "Mission": "IYK-CHD (Std.)",
            "Maximum BHP": maximum_bhp,
            "Maximum RPM": maximum_rpm,
            "Minimum RPM": minimum_rpm,
            "BSFC": bsfc,
            "%BHP": percent_bhp,
            "FF": ff,
            "TAS": tas,
            "Time": "00:15",
            "Fuel": fuel,
            "Distance": dist,
        }

        # Append data to list of rows
        rows.append(data)

    # Create dataframe
    df = pd.DataFrame(rows, columns=header.keys())

    return df

def climb(args: argparse.Namespace):

    case = {
        "airplanes": [
            Path(r"D:\Users\jgros\Documents\Github\atlas\src\telos\data\airplanes\c150m.toml"),
            Path(r"D:\Users\jgros\Documents\GitHub\atlas\src\telos\data\airplanes\c152.toml"), 
            Path(r"D:\Users\jgros\Documents\GitHub\atlas\src\telos\data\airplanes\aa5a.toml"),
            Path(r"D:\Users\jgros\Documents\GitHub\atlas\src\telos\data\airplanes\aa5b.toml"),
        ]
    }

    header = {
        "Airplane": "None",
        "Mission": "None",
        "h_0": "ft",
        "h_1": "ft",
        "ROC_0": "ft/min",
        "ROC_1": "ft/min",
        "t_0": "hh:mm",
        "t_1": "hh:mm",
        "Maximum BHP": "bhp",
        "BSFC": "lb/hp-hr",
        "%BHP": "percent",
        "FF": "gph",
        "TAS": "knots",
        "Time": "hh:mm",
        "Fuel": "gal",
        "Distance": "nmi",
    }

    rows = [header]

    for i in case["airplanes"]:

        with open(i, "rb") as f:
            airplane = tomllib.load(f)

        name = airplane["name"]

        data = {
            "Airplane": name,
            "Mission": "IYK-CHD (Std.)",
            "h_0": None,
            "h_1": None,
            "Maximum BHP": None,
            "BSFC": None,
            "%BHP": None,
            "FF": None,
            "TAS": None,
            "Time": None,
            "Fuel": None,
            "Distance": None,
        }

        rows.append(data)

    df = pd.DataFrame(rows, columns=header.keys())

    return df

def cruise(args: argparse.Namespace):

    df = pd.DataFrame()

    return df

def loiter(args: argparse.Namespace):

    df = pd.DataFrame()

    return df

def reserve(args: argparse.Namespace):

    df = pd.DataFrame()

    return df

def shutdown(args: argparse.Namespace):

    df = pd.DataFrame()

    return df

def summary():
    return None

def main():

    try:

        # Command line arguments.
        parser = argparse.ArgumentParser(description=f"{telos.__title__} {telos.__version__}", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
        parser.add_argument("-i", "--input", type=Path, required=True, help="specifies the input file")
        parser.add_argument("-o", "--output", type=Path, required=True, help="specifies the output Excel workbook (.xlsx)")
        # parser.add_argument("--case", type=Path, required=True, help="specifies the input case file (.toml)")

        args = parser.parse_args()

        df_startup = startup(args)
        df_climb = climb(args)
        df_cruise = cruise(args)
        df_loiter = loiter(args)
        df_reserve = reserve(args)
        df_shutdown = shutdown(args)

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