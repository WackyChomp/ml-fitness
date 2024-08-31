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
# Combine above 
files = glob("../../data/raw/MetaMotion/*.csv")   # gets all files from directory

def read_data_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()
    acc_set = 1
    gyr_set = 1

    for f in files:
        data_path = '../../data/raw/MetaMotion'
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

    acc_df.index = pd.to_datetime(acc_df['epoch (ms)'], unit='ms')
    gyr_df.index = pd.to_datetime(gyr_df['epoch (ms)'], unit='ms')


    del acc_df['epoch (ms)']
    del acc_df['time (01:00)']
    del acc_df['elapsed (s)']

    del gyr_df['epoch (ms)']
    del gyr_df['time (01:00)']
    del gyr_df['elapsed (s)']

    return acc_df, gyr_df

acc_df, gyr_df = read_data_from_files(files)

# --------------------------------------------------------------
# Merging datasets

#data_merged = pd.concat([acc_df.iloc[:,:3], gyr_df], axis=1)               # doesn't work

data_merged = pd.concat([acc_df.iloc[:,:3].drop_duplicates(), gyr_df], axis=1)

data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "participant",
    "label",
    "category",
    "set"
]

# Trying to see if values were missed
#data_merged['label'].unique()
#data_merged[data_merged['label'] == 'A']


# --------------------------------------------------------------
# Resample data based on frequency
# Only shows rows based on frequency increments

#data_merged[:1000].resample(rule='200ms').mean(numeric_only=True)

#data_merged.columns

# 'label', 'participant', 'category', 'set'

sampling = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "participant": "last",
    "label": "last",
    "category": "last", 
    "set": "last",
}

#data_merged[:1000].resample(rule='200ms').apply(sampling)
resampled_data_merged = data_merged[:1000].resample(rule='200ms').apply(sampling)

days = [g for n, g in data_merged.groupby(pd.Grouper(freq='D'))]

# Saving on computing resources and avoid potential crashes
final_data_resampled = pd.concat([df.resample(rule='200ms').apply(sampling).dropna() for df in days])


#final_data_resampled.head()

final_data_resampled.info()

# convert 'set' column from data type "float" to "int"
final_data_resampled['set'] = final_data_resampled['set'].astype(int)

# --------------------------------------------------------------
# Export dataset
# Pickle is ideal for timestamp

final_data_resampled.to_pickle('../../data/interim/01_data_processed.pkl')
