import telos
import argparse
import tomllib
from pathlib import Path
from importlib.resources import files

def main():

    parser = argparse.ArgumentParser(description=f"{telos.__title__} {telos.__version__}", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # parser.add_argument("-i", "--input", type=str, required=True, help="input file")
    # parser.add_argument("-o", "--output", type=str, required=True, help="output file")

    parser.add_argument("--case", type=str, required=True, help="specifies the input case file (.toml)")

    args = parser.parse_args()

    with open(args.case, "rb") as f:
        case = tomllib.load(f)

    for i in case["airplanes"]:

        toml_file = files("telos.data.airplanes").joinpath(i).with_suffix(".toml")

        with toml_file.open("rb") as f:
            data = tomllib.load(f)

        print(data["name"])

        # Takeoff distance

        print(data["takeoff_ground_roll_distance"]["coefficients"])

        # Climb

        # Cruise speed

        # Cruise range

        # Landing distance