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
# MatPlotLib settings (establish settings in the beginning gets applied throughout)

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
  # Resetting index and sorting values will group 
  # particpants properly and ensure consistent plotting


#participant_df = df.query('label == "bench"').reset_index()
#participant_df = df.query('label == "bench"').sort_values('participant')
participant_df = df.query('label == "bench"').sort_values('participant').reset_index()


fig, ax = plt.subplots()
participant_df.groupby(['participant'])['acc_y'].plot()
ax.set_xlabel('samples')
ax.set_ylabel('acc_y')
plt.legend()


# --------------------------------------------------------------
# Plot multiple axis of a single lable and participant
# [[]] - converts to dataframe

label = 'squat'
participant = 'A'
all_axis_df = df.query(f'label == "{label}"').query(f'participant == "{participant}"').reset_index()


fig, ax = plt.subplots()
all_axis_df[['acc_x', 'acc_y', 'acc_z']].plot(ax=ax)
ax.set_xlabel('samples')
ax.set_ylabel('acc_y')
plt.legend()


# --------------------------------------------------------------
# Plot all combinations for each lable/participant
labels = df['label'].unique()
participants = df['participant'].unique()     # notice that participant E is missing (revisit make_dataset.py)

for label in labels:
  for participant in participants:
    all_axis_df = (
      df.query(f'label == "{label}"')
      .query(f'participant == "{participant}"')
      .reset_index()
    )

    if len(all_axis_df) > 0:

      fig, ax = plt.subplots()
      all_axis_df[['acc_x', 'acc_y', 'acc_z']].plot(ax=ax)
      ax.set_xlabel('samples')
      ax.set_ylabel('acc_y')
      plt.title('f{label} ({participant})'.title())
      plt.legend()


# --------------------------------------------------------------
# Combine plots in one figure

