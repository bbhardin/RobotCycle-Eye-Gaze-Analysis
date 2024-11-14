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
for i in range(1, 100): #len(pitches)):
    d_x = (pitches[i] - pitches[i-1])
    d_y = (yaws[i] - yaws[i-1])
    eye_move_dists.append(math.sqrt((d_x*d_x) + (d_y*d_y))) # Distance moved of the eyes at each time step
    #gaze_loc.append([gaze_loc[i-1, 0] + d_x, gaze_loc[i-1, 1] + d_y]) # Position of eyes over time. Starts at (0,0)
    gaze_loc_x.append(gaze_loc_x[i-1] + d_x)
    gaze_loc_y.append(gaze_loc_y[i-1] + d_y)

# slope = pd.Series(np.gradient(pitches), times, name='slope')
# dists = pd.Series(eye_move_dists, times, name='dists')
# vals = pd.Series(pitches, times, name='pitches')
locs = pd.Series(gaze_loc_x, gaze_loc_y, name='loc')
#slope = pd.Series([1,2,3], [1,2,3])
fig = plt.figure()
plt.isinteractive = False
plt.plot(locs.index, locs.values, '-p', label='loc')
# plt.plot(dists.index, dists.values, "-b", label='dist')
# plt.plot(slope.index, slope.values, "-r", label='derivative pitch')
# plt.plot(vals.index, vals.values, "-g", label='pitches')
plt.legend()
fig.show()