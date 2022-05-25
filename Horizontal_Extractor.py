# This code is designed to make x,y list from .msh5 file for making a 1D extract for rows or columns (not diagonals).
# Author: Richard Bell
# Last edit: 8-5-21

#-------------------------------------Library Import----------------------------------------------------------------
from __future__ import print_function
from spike.FTICR import FTICRData
import os
import numpy as np

#------------------------------------Selecting and Importing Data--------------------------------------------------
# Section to set incoming file and outgoing file. Also defines parameters for m/z values.
# This section contains all fields to be edited for use from file to file
parent_directory = r"C:\Richard\2D_Data\12-7-21_2D_MALDI\Main"  # Directory containing outfile.msh5
import_name = (parent_directory + os.sep + '2D_IRMPD_MALDI_outfile.msh5')  # Name of incoming file
export_name = (parent_directory + os.sep + 'BK_ROW.txt')
temp_file = (parent_directory + os.sep + 'temp.csv')

spike_data = FTICRData(name=import_name, mode="onfile", debug=1, group = 'resol1')

dimension = "row"
mz = 1061.603593

mzmax = 2000
mzmin = 154

#------------------------------------Converting to index------------------------------------------------------------
# This section will convert the desired m/z into an index for accessing the row or column later. If uses if, elif, and
# else to decide if it is a row or column being extracted. If row or column is not selected, it will stop.
if dimension == "row":
    index = int(spike_data.axis1.mztoi(mz))
    print("Index:", index)
    print("m/z:", spike_data.axis1.itomz(index))
elif dimension == "column":
    index = int(spike_data.axis2.mztoi(mz))
    print("Index:",index)
    print("m/z:", spike_data.axis2.itomz(index))
else:
    raise Exception("Must extract row or column")

#------------------------------------Extract and Export-----------------------------------------------------------
# This section will generate a blank list, extract the xy data for the set index, and save as a temporary file. That
# will be re-imported (a step where it is directly set as a list or np array would be a future improvement) as a numpy
# array. The array will be iterated through and all values within the set m/z range will be added to an outgoing list.
# That list is then saved as the set export name.

xy_list = []

if dimension == "row":
    extract_data = spike_data.row(index)
    extract_data.unit = 'm/z'
    extract_data.save_csv(name = temp_file)
elif dimension == "column":
    extract_data = spike_data.col(index)
    extract_data.unit = 'm/z'
    extract_data.save_csv(name = temp_file)

extract_import = np.loadtxt(fname=temp_file, comments='#', delimiter=',')
np.round(extract_import, 2)

for row in extract_import:
    if row[0] <= mzmax and row[0] >= mzmin and row[1] >= 0 :
        point = [row[0],row[1]]
        xy_list.append(point)

np.savetxt(export_name, xy_list, delimiter=",")


