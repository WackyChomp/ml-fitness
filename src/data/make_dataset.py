import pandas as pd
from glob import glob

# ------------------------------------------------------------------------------------------
# Read single CSV file

single_file_1 = pd.read_csv('../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv')
single_file_2 = pd.read_csv('../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv')

# ------------------------------------------------------------------------------------------
# List all data from ./data/raw
files = glob("../../data/raw/MetaMotion/*.csv")   # gets all files from directory
len(files)

# ------------------------------------------------------------------------------------------
# Extract strings from filename and append to dataframe
    # (participant / label / category)

# see splits between '-' with --- f.split('-')

data_path = '../../data/raw/MetaMotion'
f = files[0]    # 1st dataset of the directory

f.split('-')      # splitting the filename into list

participant = f.split('-')[0].replace(data_path, "").replace('\\', "")          # remove "\\" from the path
label = f.split('-')[1]
category = f.split('-')[2].strip('123').strip('_MetaWear_2019')       # removes (1-3) numbers that appear at the end of a category


df = pd.read_csv(f)
df['participant'] = participant
df['label'] = label
df['category'] = category
# ------------------------------------------------------------------------------------------
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
        df['set'] = acc_set
        acc_set += 1
        acc_df = pd.concat([acc_df, df])
    if "Gyroscope" in f:
        df['set'] = gyr_set
        gyr_set += 1
        gyr_df = pd.concat([gyr_df, df])


acc_df[acc_df['set'] == 2]         # Find specific set based on append increment

# ------------------------------------------------------------------------------------------
# Datetimes conversion
acc_df.info()

# pd.to_datetime(df['epoch (ms)'], unit='ms')     # convert to "datetime" data type

acc_df.index = pd.to_datetime(acc_df['epoch (ms)'], unit='ms')
gyr_df.index = pd.to_datetime(gyr_df['epoch (ms)'], unit='ms')

# remove time related columns after setting time to index for time series data
del acc_df['epoch (ms)']
del acc_df['time (01:00)']
del acc_df['elapsed (s)']

del gyr_df['epoch (ms)']
del gyr_df['time (01:00)']
del gyr_df['elapsed (s)']


# --------------------------------------------------------------
# Merging datasets



# --------------------------------------------------------------
# Export dataset

