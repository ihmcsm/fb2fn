import argparse
import pandas as pd
import sqlite3
import os
from os import system


system("clear||cls")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Take your weight logs from Fitbit's Takeout and bring them into FitNotes"
    )
    parser.add_argument(
        "-input",
        required=False,
        type=str,
        default="weight.csv",
        help="Fitbit exported weight.csv location. You will find this file in the PhysicalActivity_GoogleData folder of your Takeout. Defaults to working directory.",
    )
    parser.add_argument(
        "-output",
        required=False,
        type=str,
        default="FitNotes_Backup.fitnotes",
        help="FitNote backup file (FitNotes_Backup.fitnotes) location. Defaults to working directory.",
    )
    args = parser.parse_args()

    in_file = args.input
    out_file = args.output

print(
    "Please make a backup of your FitNotes before trying this, I'm not responsible if you burn down your house."
)
user_input = input("Do you want to proceed? (y/n): ")

if user_input.lower() == "y":
    print("Proceeding...")
    # Load FitNotes backup
    conn = sqlite3.connect(out_file)
    c = conn.cursor()
    # Take the raw FitBit data and make it suitable for importing into sqlite table
    col_order = ["measurement_id", "date", "time", "value"]
    fitbit_data = pd.read_csv(in_file)
    # Remove columns that aren't required & split timestamps into two seperate columns
    fitbit_data.drop(columns=["data source"], inplace=True)
    fitbit_data["timestamp"] = fitbit_data["timestamp"].str.replace("Z", "")
    new_columns = fitbit_data["timestamp"].str.split("T", n=1, expand=True)
    fitbit_data["date"] = new_columns[0]
    fitbit_data["time"] = new_columns[1]
    fitbit_data.drop(columns=["timestamp"], inplace=True)
    # Convert weight from raw grams into rounded figures
    fitbit_data["weight grams"] = round(fitbit_data["weight grams"] / 1000, 1)
    fitbit_data.rename(columns={"weight grams": "value"}, inplace=True)
    # Insert measurement_id (value should be 1, hence checking entries after as it may show up under Body Fat instead) sort some columns and save to a temp file which will be removed later
    fitbit_data.insert(0, "measurement_id", "1")
    fitbit_data = fitbit_data.reindex(columns=col_order)
    fitbit_data.to_csv("temp.csv", index=False)
    # Write data from the temp file to sqlite database
    temp_file = pd.read_csv("temp.csv")
    temp_file.to_sql("MeasurementRecord", conn, if_exists="append", index=False)
    # Remove temp file before notifing user and then exit
    os.remove("temp.csv")
    print(
        "Conversion completed! Import your backup into FitNotes and double check the entries are correct."
    )
elif user_input.lower() == "n":
    print("Exiting.")
else:
    print("Invalid input. Please enter 'y' or 'n'.")