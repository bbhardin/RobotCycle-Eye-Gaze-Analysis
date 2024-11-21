import projectaria_tools.core.mps as mps

gaze_path = "/Users/Ben/Downloads/mps_Jumana_vrs/eye_gaze/general_eye_gaze.csv"
gaze_cpf = mps.read_eyegaze(gaze_path)
pitches, yaws, times = zip(*[(obj.pitch, obj.yaw, obj.tracking_timestamp) for obj in gaze_cpf])
#print(gaze_cpf)
#exit


# Set default eye gaze depth for 3D points to 1 meter
#depth_m = 1.0
#gaze_point_cpf = mps.get_eyegaze_point_at_depth(gaze_cpf[1].yaw, gaze_cpf[1].pitch, depth_m)

# Query Eye Gaze data at a desired timestamp
# For this example we use an eyegaze data timestamp
# You can also use a VRS timestamp (i.e timestamp from a loop reading all the images)

#query_timestamp_ns = int(gaze_cpf[1].tracking_timestamp.total_seconds() * 1e9)

#eye_gaze_info = get_nearest_eye_gaze(gaze_cpf, query_timestamp_ns)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

eye_move_dists = [0]
gaze_loc = [[0,0]]
gaze_loc_x = [0]
gaze_loc_y = [0]
for i in range(1, 250):#len(pitches)):
    d_x = (pitches[i] - pitches[i-1])
    d_y = (yaws[i] - yaws[i-1])
    eye_move_dists.append(math.sqrt((d_x*d_x) + (d_y*d_y))) # Distance moved of the eyes at each time step
    #gaze_loc.append([gaze_loc[i-1, 0] + d_x, gaze_loc[i-1, 1] + d_y]) # Position of eyes over time. Starts at (0,0)
    #gaze_loc_x.append(gaze_loc_x[i-1] + d_x)
    #gaze_loc_y.append(gaze_loc_y[i-1] + d_y)
    gaze_loc_x.append(pitches[i])
    gaze_loc_y.append(yaws[i])

fixation_indices = [24, 41, 48, 120, 130, 147, 153, 162, 164, 174, 179, 185, 189, 197, 289, 295, 309, 335, 345, 373, 379, 385, 396, 399, 404, 412, 429, 434, 437, 441, 443, 447, 455, 464, 466, 474, 479, 482, 488, 493, 499, 504, 537, 543, 578, 637, 640, 688, 801, 828, 861, 877, 923, 939, 949, 970, 984, 992]
fixation_point_x = []
fixation_point_y = []
#time_at_fixation = []
#time_at_fixation.append(fixation_indices[0])
for i in fixation_indices:
    if (i > 200):
        break
    fixation_point_x.append(gaze_loc_x[i])
    fixation_point_y.append(gaze_loc_y[i])
    #if (i > 0):
        #time_at_fixation.append(fixation_indices[i] - fixation_indices[i-1])
        # Ok there's an issue here because it does count the zeros in between the fixations... so that's a problem
            # I could just create an array to drop the zeros. Like once we've started counting, then just drop the zeros.
        # TODO: multiply by the time between measurements in our experiment. Currently this assumes 1ms between samples which is obviously wrong


# slope = pd.Series(np.gradient(pitches), times, name='slope')
# dists = pd.Series(eye_move_dists, times, name='dists')
# vals = pd.Series(pitches, times, name='pitches')

# ANALYZE HORIZONTAL GAZE DISPERTION
#   Horizontal is the yaw component
#   Want to measure variation with a 10s sliding window (30 frames)

vars = []
for i in range(30, len(yaws)):
    window = yaws[i-30:i]
    vars.append(np.var(window))

fig = plt.figure()
plt.plot(vars)
plt.show()

exit(0)

locs = pd.Series(gaze_loc_x, gaze_loc_y, name='loc')
locs2 = pd.Series(fixation_point_x, fixation_point_y, name='loc2')

#slope = pd.Series([1,2,3], [1,2,3])
fig = plt.figure()
plt.isinteractive = False
plt.plot(locs.index, locs.values, '-p', label='fix')
plt.plot(locs2.index, locs2.values, '-r', label='loc')
# plt.plot(dists.index, dists.values, "-b", label='dist')
# plt.plot(slope.index, slope.values, "-r", label='derivative pitch')
# plt.plot(vals.index, vals.values, "-g", label='pitches')
plt.legend()
fig.show()