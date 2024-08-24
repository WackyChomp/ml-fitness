import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file

single_file_1 = pd.read_csv('../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv')
single_file_2 = pd.read_csv('../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv')

# --------------------------------------------------------------
# List all data from ./data/raw
files = glob("../../data/raw/MetaMotion/*.csv")   # gets all files from directory
len(files)

# --------------------------------------------------------------
# Extract strings from filename and append to dataframe
    # (participant / label / category)

# see splits between '-' with --- f.split('-')

data_path = '../../data/raw/MetaMotion'
f = files[2]    # 1st dataset of the directory

f.split('-')      # splitting the filename into list

participant = f.split('-')[0].replace(data_path, "").replace('\\', "")          # remove "\\" from the path
label = f.split('-')[1]
category = f.split('-')[2].strip('123').strip('_MetaWear_2019')       # removes (1-3) numbers that appear at the end of a category


df = pd.read_csv(f)
df['participant'] = participant
df['label'] = label
df['category'] = category
# --------------------------------------------------------------
# Read all files

acc_df = pd.DataFrame()
gyr_df = pd.DataFrame()

acc_set = 1         # used to create unique identifier for each specific set
gyr_set = 1

for f in files:
    participant = f.split('-')[0].replace(data_path, "").replace('\\', "")          # remove "\\" from the path
    label = f.split('-')[1]
    category = f.split('-')[2].strip('123').strip('_MetaWear_2019')       # removes (1-3) numbers that appear at the end of a category

    df = pd.read_csv(f)

    df['participant'] = participant
    df['label'] = label
    df['category'] = category

    if "Accelerometer":
        acc_df = pd.concat([acc_df, df])
    if "Gyroscope" in f:
        gyr_df = pd.concat([gyr_df, df])

# --------------------------------------------------------------
# Datetimes conversion



# --------------------------------------------------------------
# Merging datasets



# --------------------------------------------------------------
# Export dataset

