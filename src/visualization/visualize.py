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
# MatPlotLib settings

mpl.style.use('seaborn-v0_8-deep')
mpl.rcParams['figure.figsize'] = (20,5)
mpl.rcParams['figure.dpi'] = 100
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
# Compare set types (medium vs. heavy)

# query
category_df = df.query("label == 'squat'").query("participant == 'A'").reset_index()


# groupby plot
fig, ax = plt.subplots()
category_df.groupby(['category'])['acc_y'].plot()
ax.set_xlabel('samples')
ax.set_ylabel('acc_y')
plt.legend()

# --------------------------------------------------------------
# Compare participants


# --------------------------------------------------------------
# Plot multiple axis



# --------------------------------------------------------------
# Combine plots in one figure

