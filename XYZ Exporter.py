from __future__ import print_function
from spike.FTICR import FTICRData
import os
import numpy as np

# This code is designed to make x,y,z list from .msh5 file for making a heatmap in igor.
# Modified from original for data reduction by removing points with intensities below set point

# True False relationship used for sample downsizing. In practice, we want to remove 3D points when their intensity
# is below a set point (a count of 5000)

# ---------------------Selecting and Importing Data--------------------------------------------------
# Section to set incoming file as well as name for outgoing file.
# This section contains the fields to be edited for use from file to file
parent_directory = r"C:\Path\Path\File"                                                                                 # Directory containing outfile.msh5
import_name = (parent_directory + os.sep + 'NAME.msh5')                                                                 # Name of incoming file
export_name = (parent_directory + os.sep + 'NAME.txt')                                                                  # Name of file to be read into Igor
temp_file = (parent_directory + os.sep + 'temp.csv')                                                                    # Temp file for iterating through rows

spike_data = FTICRData(name=import_name, mode="onfile", debug=1, group = 'resol2')                                      # importing data into SPIKE programing

# Defines m/z window for exporting.
F2mzmin = 160                                                                                                           # The low m/z value in F2
F2mzmax = 1600                                                                                                          # The high m/z value in F2
F1mzmin = 1000                                                                                                          # The low m/z value in F1
F1mzmax = 1600                                                                                                          # The high m/z value in F1
F1indexmin = int(spike_data.axis1.mztoi(F1mzmax))                                                                       # Index for HIGH m/z in F1 (Calculated)
F1indexmax = int(spike_data.axis1.mztoi(F1mzmin))                                                                       # Index for LOW m/z in F1 (Calculated)
I_setpoint = 50000                                                                                                      # Minimum intensity to be recorded for export
# ---------------------------------------------------------------------------------------------------------------------
# Conversion Execution
# List Generation : Set initial values for variables
indexlist = range(F1indexmin, F1indexmax + 1)                                                                            # List of F1 indexes to iterate through
xyz_list = []                                                                                                            # Blank list for triplets for x,y,z output
xyz_list_reduced = []                                                                                                    # Initial intensity max

# Iterator: following xyz list, all x,z pairs in an index will be found and an xyz triplet will be formed
for index in indexlist:                                                                                                  # For loop to iterate through all indexes
    index_mz = spike_data.axis1.itomz(index)                                                                             # Finds F1 m/z from index for y
    row_data = spike_data.row(index)                                                                                     # Takes horizontal extract at current index
    row_data.unit = 'm/z'                                                                                                # Sets x units to m/z instead of native index
    row_data.save_csv(
        name=temp_file)                                                                                                  # Exports horizontal extract to csv
    row_data = np.loadtxt(fname=temp_file, comments='#', delimiter=',')                                                  # Re-imports horizontal extract as np array
    print("Point Creation: Index ", index, " of ", F1indexmax, ": m/z = ", index_mz)                                     # Updates output status of what index is being read
    for row in row_data:                                                                                                 # For loop to iterate through all xz pairs in extract
        if row[0] <= F2mzmax and row[0] >= F2mzmin:                                                                      # Removes all x values outside of defined F2 range
            if row[1] > I_setpoint:
                point = [row[0], index_mz, row[1]]                                                                           # Creates a triplet for x,y,z point
                xyz_list.append(point)                                                                                       # Adds above triplet to list of triplets
            else:
                pass

# Wrap up: Export list and let user know process is done.
outgoing_array = np.array(xyz_list)                                                                                      # Makes a numpy array from list of triplets
np.savetxt(export_name, outgoing_array, delimiter=",")                                                                   # Exports numpy array as .txt file
print('done')                                                                                                            # Returns "done" to user



# Running List To Do
#   1. Reconfigure the downsizing to be absolute rather than as  a percentage of max. This would greatly reduce time for
#      processing. Data points with low I could simply not be added to the list rather than added and removed.
#   2. Reconfigure the way rows are gathered. It would be nice to not have to export rows to cv then reimport them in as
#      a numpy array. Can we simply say I want row x as a numpy array (or even a list)?