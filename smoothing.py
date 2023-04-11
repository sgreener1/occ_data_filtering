import json
import numpy as np

FILENAME = "NCSU_count_data.json"
SMOOTHING_FACTOR = 1

file = open(FILENAME)
data = json.load(file)

filtered_data = {}
for room in data:
    print(room)
    filtered_data[room] = {}
    counts = data[room].values()
    timestamps = data[room].keys()
    data_array = np.array(list(map(int, counts)))
    timestamp_array = list(map(str, timestamps))
    diff_array = np.diff(data_array)
    std_of_diff = np.std(diff_array)
    allowable_diff = SMOOTHING_FACTOR * std_of_diff
    curr_room_array = [len(data_array)]
    print("allowable difference between points is: ", allowable_diff)
    for x in range(0, len(diff_array)):
        curr_room_array[0] = int(data_array[0])
        if (x > 0 and x < len(diff_array)-1):
            lower_val = data_array[x-1]
            current_val = data_array[x]
            upper_val = data_array[x+1]
            lower_diff = abs(lower_val - current_val)
            upper_diff = abs(upper_val - current_val)
            if (lower_diff > allowable_diff and upper_diff > allowable_diff):
                new_val = round(abs((lower_val + upper_val) / 2))
                curr_room_array.append(int(new_val))
            else:
                curr_room_array.append(int(current_val))
    for y in range(0, len(curr_room_array)):
        filtered_data[room][timestamp_array[y]] = curr_room_array[y]

filtered_json = json.dumps(filtered_data, indent=4)
with open("filtered_data.json", "w") as outfile:
    outfile.write(filtered_json)

file.close()