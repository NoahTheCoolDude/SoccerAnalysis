import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats

#load the original df, calling it OG for original
OGdf = pd.read_csv('C:/Users/Admin/Downloads/Sample_Game_1_RawEventsData.csv')

#calculate the delta t (s) column
OGdf['delta t (s)'] = OGdf['End Time [s]'].diff()  

#.diff takes the current value and subtracts the previous 
# row's value to find the delta t

# making plot to show histogram (frequencies) of the length of each action

#begin by removing NA values from the delta t column
deltat = OGdf['delta t (s)'].dropna() #.dropna() removes na values, and would replace it with the value in the ()

plt.figure(figsize=(10,6))
plt.hist(deltat, bins = 100, color = 'skyblue', edgecolor = 'black')

plt.title('frequency of the action durations for sample game 1')
plt.xlabel('duration of action, seconds')
plt.ylabel('frequency of duration')
plt.grid(True, linestyle = '--', alpha = 0.6)

plt.show()


# --------------------------------------------------

# identify each action (ball in play or play isn't stopped)

action_durations = []
last_set_piece_time = None

# iterate through the DataFrame to find consecutive 'SET PIECE' events
for i, row in OGdf.iterrows():
    # Check if the event type is a 'SET PIECE'
    if row.get('Type') == 'SET PIECE':
        # If we have a stored start time from the previous SET PIECE, calculate the duration
        if last_set_piece_time is not None:
            duration = row['Start Time [s]'] - last_set_piece_time
            if duration > 0:
                action_durations.append(duration)
        
        # Update the last set piece time to the start of the current one,
        # making it the start time for the next action sequence.
        last_set_piece_time = row['Start Time [s]']


# Convert the list of durations into a pandas Series for analysis
action_lengths = pd.Series(action_durations)


# --- 1. Calculate the Empirical CDF ---
# This is the CDF generated directly from your data points.
x_ecdf = np.sort(action_lengths)
y_ecdf = np.arange(1, len(x_ecdf) + 1) / len(x_ecdf)


# --- 2. Fit a Gamma Distribution to the Data ---
# Use scipy's stats module to find the best-fit gamma distribution parameters.
shape, loc, scale = stats.gamma.fit(action_lengths, floc=0)


# --- 3. Create the Plot ---
plt.figure(figsize=(12, 7))

# Plot the Empirical CDF from your data
plt.plot(x_ecdf, y_ecdf, marker='.', linestyle='none', label='CDF')

# Plot the theoretical CDF from the fitted gamma distribution
x_fit = np.linspace(action_lengths.min(), action_lengths.max(), 200)
y_fit = stats.gamma.cdf(x_fit, shape, loc=loc, scale=scale)
plt.plot(x_fit, y_fit, 'r-', lw=2, label=f'Fitted Gamma CDF')

# Add labels and a title to make the plot informative
plt.title('Cumulative Distribution of Soccer Action Durations')
plt.xlabel('Duration of Action (seconds)')
plt.ylabel('Cumulative Probability')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Display the plot
plt.show()

print(f"the total amount of actions is: {len(action_lengths)}")