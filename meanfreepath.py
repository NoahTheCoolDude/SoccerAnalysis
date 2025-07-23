import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# pitch dimensions in meters
PITCH_X = 100
PITCH_Y = 70


# simply change the file directory to the other sample game to switch between analysis for both
OGdf = pd.read_csv('C:/Users/ruder/Downloads/Sample_Game_2_RawEventsData.csv')

# begin by converting the decimal coordinates to meters so that we can find the distance between two points 
# in terms of meters, just like the original study
OGdf['Start X [m]'] = OGdf['Start X'] * PITCH_X
OGdf['Start Y [m]'] = OGdf['Start Y'] * PITCH_Y
OGdf['End X [m]'] = OGdf['End X'] * PITCH_X
OGdf['End Y [m]'] = OGdf['End Y'] * PITCH_Y


# first, analyzing mean free path between ALL actions

# .shift(1) gets the end coordinates of the previous event on the current row
OGdf['Prev End X [m]'] = OGdf['End X [m]'].shift(1)
OGdf['Prev End Y [m]'] = OGdf['End Y [m]'].shift(1)

# Calculate the distance between the end of the previous event and the start of the current one with the distance formula
OGdf['Mean Free Path [m]'] = np.sqrt(
    (OGdf['Start X [m]'] - OGdf['Prev End X [m]'])**2 +
    (OGdf['Start Y [m]'] - OGdf['Prev End Y [m]'])**2
)

# Calculate mean and standard deviation for the mean free path
mfp_mean = OGdf['Mean Free Path [m]'].mean()
mfp_std = OGdf['Mean Free Path [m]'].std()


# second, analyzing mean free path between ONLY successful passes

# identify passes that are followed by another pass
is_pass = OGdf['Type'] == 'PASS'
is_followed_by_pass = is_pass.shift(-1).fillna(False) # if the next 'Type' value isn't a pass, return false
consecutive_passes_mask = is_pass & is_followed_by_pass

# filter the data to get only the first pass in a consecutive sequence
consecutive_passes = OGdf[consecutive_passes_mask].copy()  #.copy creates a whole new dataframe called consecutive_passes

# use the distance formula to find the distances between successful passes
consecutive_passes['Pass Length [m]'] = np.sqrt(
    (consecutive_passes['End X [m]'] - consecutive_passes['Start X [m]'])**2 +
    (consecutive_passes['End Y [m]'] - consecutive_passes['Start Y [m]'])**2
)

# calculate mean and standard deviation for these pass lengths
pass_mean = consecutive_passes['Pass Length [m]'].mean()
pass_std = consecutive_passes['Pass Length [m]'].std()


# making the histograms:

# Create a figure with two separate subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Mean Free Path (barebones)
ax1.set_title(f"$\\lambda$ of consecutive actions, game 2")
ax1.hist(OGdf['Mean Free Path [m]'].dropna(), bins=50)
ax1.set_xlabel("Distance Between Events (m)")
ax1.set_ylabel("Frequency")

# Plot 2: Consecutive Pass Lengths (barebones)
ax2.set_title(f"$\\lambda$ of pass lengths, game 2")
ax2.hist(consecutive_passes['Pass Length [m]'], bins=50)
ax2.set_xlabel("Distance Between Events (m)")
ax2.set_ylabel("Frequency")

# Show the plots
plt.show()


print(f"the average length between consecutive actions is {mfp_mean}")
print(f"the standard deviation between consecutive actions is {mfp_std}")
print(f"the average length between successful passes is {pass_mean}")
print(f"the standard deviation between successful passes is {pass_std}")
