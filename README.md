# fb2fn
Take your weight logs from Fitbit's Takeout and bring them into FitNotes

## Installation

Manual installation:

```sh
gh repo clone ihmcsm/fb2fn
```


## Dependencies

You may need to install 'pandas' before running the script by running:
```sh
pip install pandas
```


## Prerequisites

### Exported Fitbit weight.csv
You will need to have your FitBit data exported from Google Takeout (takeout.google.com)

Follow the instructions (I exported everything) and wait for the zip(s) to arrive. It can be hours or days you never know.

Once you have your Takeout, find the weight.csv file. As of Nov 2025 it is located in the Takeout/Fitbit/Physical Activity_GoogleData folder.

Place a copy of the weights.csv file in the working directory.

### Exported FitNotes backup
In the FitNotes app, press the hamburger button and go into Settings.

Scroll to Backup and select Save Backup (without timestamp in filename).

Save the FitNotes_Backup.fitnotes to an apropriate location and then move into the working directory.


## Usage

Just run the script and follow the prompts:

```sh
cd fb2fn
python3 fb2fn.py
```
