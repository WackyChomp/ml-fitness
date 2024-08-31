import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# --------------------------------------------------------------
# Load data
df = pd.read_pickle('../../data/interim/01_data_processed.pkl')


# --------------------------------------------------------------
# Plot single column

set_df = df[df['set'] == 1]

plt.plot(set_df['acc_y'])
plt.plot(df['acc_y'])

# --------------------------------------------------------------
# Plot all exercise types



# --------------------------------------------------------------
# Compare set types


# --------------------------------------------------------------
# Compare participants


# --------------------------------------------------------------
# Plot multiple axis



# --------------------------------------------------------------
# Combine plots in one figure

