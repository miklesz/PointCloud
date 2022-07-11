import matplotlib.pyplot as plt

FILE = 'profile_list_snapshot.csv'

with open(FILE) as f:
    times = f.read()
times_list = times.split()
times_list_float = [float(time) for time in times_list]
# print(times_list_float)

# x = []
# per_seconds = [[]]*296
# per_seconds = [[]]*10
per_seconds = [[] for i in range(296)]
level_60 = [60]*296

# for time_float in times_list_float:
for time_float in times_list_float:
    second = int(time_float)
    per_seconds[second].append(time_float)

fps_per_seconds = [len(per_second) for per_second in per_seconds]

diff_per_seconds = []
for per_second in per_seconds:
    max_diff = 0
    for frame_time_i in range(len(per_second)-1):
        if per_second[frame_time_i+1]-per_second[frame_time_i]>max_diff:
            max_diff = per_second[frame_time_i+1]-per_second[frame_time_i]
    # diff_per_seconds = 60/max_diff
    diff_per_seconds.append(1/max_diff)

print(diff_per_seconds)

plt.plot(fps_per_seconds)
plt.plot(level_60)
plt.plot(diff_per_seconds)
plt.xlabel('time [s]')
plt.ylabel('fps')
plt.grid(which='both')
plt.minorticks_on()
plt.show()