import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display     # display dataframes within a loop

# --------------------------------------------------------------
# Load data
df = pd.read_pickle('../../data/interim/01_data_processed.pkl')


# --------------------------------------------------------------
# Plot single column

set_df = df[df['set'] == 1]

plt.plot(set_df['acc_y'])
plt.plot(df['acc_y'])

plt.plot(set_df['acc_y'].reset_index(drop=True))      # reset index to show number of samples

# --------------------------------------------------------------
# Plot all exercise types

#df['label'].unique()


# Displays all the existing samples
for label in df['label'].unique():
  subset = df[df['label'] == label]
  #display(subset.head())       # display dataframe within a loop

  fig, ax = plt.subplots()

  plt.plot(subset['acc_y'].reset_index(drop=True), label=label)             # displays all samples
  #plt.plot(subset[:100]['acc_y'].reset_index(drop=True), label=label)      # displays first 100 samples

  plt.legend()
  plt.show()


# --------------------------------------------------------------
# Compare set types


# --------------------------------------------------------------
# Compare participants


# --------------------------------------------------------------
# Plot multiple axis



# --------------------------------------------------------------
# Combine plots in one figure

