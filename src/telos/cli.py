import telos
import argparse
import math
import tomllib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path
from importlib.resources import files

def main():

    # Command line arguments.
    parser = argparse.ArgumentParser(description=f"{telos.__title__} {telos.__version__}", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # parser.add_argument("-i", "--input", type=str, required=True, help="input file")
    # parser.add_argument("-o", "--output", type=str, required=True, help="output file")

    parser.add_argument("--case", type=Path, required=True, help="specifies the input case file (.toml)")

    args = parser.parse_args()

    # Open the case file.
    with open(args.case, "rb") as f:
        case = tomllib.load(f)

    h = range(0, 10000, 100)

    # Iterate over airplanes in the case file.
    for i in case["airplanes"]:

        toml_file = files("telos.data.airplanes").joinpath(i).with_suffix(".toml")

        with toml_file.open("rb") as f:
            data = tomllib.load(f)

        print(data["name"])

        # Weight & balance
        bhp = data["brake_horsepower"]["value"]
        gross_weight = data["maximum_gross_weight"]["value"]

        # Takeoff distance

        print(data["takeoff_ground_roll_distance"]["coefficients"])

        # Climb
        model = data["rate_of_climb"]["model"]
        bsfc = 0.45 # 0.45 lb/bhp/hr per Raymer
        percent_bhp = 1.00

        df = pd.DataFrame()

        df["density_altitude"] = h

        for density_altitude in h:

            x = pd.Series(
                {
                    "constant": 0,
                    "gross_weight": gross_weight,
                    "density_altitude": density_altitude,
                }
            )
            b = pd.Series(data["rate_of_climb"]["coefficients"])

            df["rate_of_climb"] = x @ b # equivalent to y = x*b^T + err

            df["time_to_climb"] = (1/b["density_altitude"])*math.log10(df["rate_of_climb"] / (b["constant"] + b["gross_weight"]*x["gross_weight"]))

            df["pph"] = bsfc*bhp*percent_bhp
            df["ff"] = df["pph"] / 6
            df["v"] = data["vy"]["value"]

            df["fuel_to_climb"] = df["ff"] * df["time_to_climb"]

            df["distance_to_climb"] = df["v"] * df["time_to_climb"]

        plt.plot(df["fuel_to_climb"], df["density_altitude"])
        plt.show()

        

        # Cruise speed

        # Cruise range

        # Landing distance