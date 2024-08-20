#file_path = "2024_07_13_S01_4mA_0.03Hz_Rotation_250K_14T_"

#with open(file_path, 'r') as file:
#    for line in file:
#       print(line.strip());

#the data file given is CSV file.

def is_new_angle(data, row_index, jump_threshold=1.0):
    if row_index <= 0 or row_index >= len(data):
        return False

    if len(data[row_index]) <= 7 or len(data[row_index - 1]) <= 7:
        return False

    current_value = data[row_index][7]
    if current_value is None:
        return False

    try:
        current_value = abs(float(current_value))
    except ValueError:
        return False

    previous_value = data[row_index-1][7]
    if previous_value is None:
        return False

    try:
        previous_value = abs(float(previous_value))
    except ValueError:
        return False

    if abs(previous_value - current_value) > jump_threshold:
        return True
    else:
        return False

def averaged_volatge(data, row_index, column_index):
    selected_data = []

    initial_value = data[row_index][column_index]
    if initial_value is not None:
        try:
            selected_data.append(float(initial_value))
        except ValueError:
            pass

    row_index += 1
    while row_index < len(data):
        choiceC = is_new_angle(data[row_index][7])
        if choiceC is False:
            try:
                selected_data.append(float(data[row_index][7]))
            except ValueError:
                pass
        if choiceC is not None:
            break
        row_index += 1


    if selected_data:
        vol_ave = sum(selected_data) / len(selected_data)
    else:
        vol_ave = 0

    return vol_ave

import csv
file_path = "2024_07_13_S01_4mA_0.03Hz_Rotation_250K_14T_"

with open(file_path, 'r') as file:
    csv_reader = csv.reader(file)
    data = list(csv_reader)

processed_data = []

for row in data:
    header_skipped = False
    if not header_skipped:
        if not row or (len(row) == 1 and not row[0].strip()):
            continue

    if 'Comment' in row[0]:
        header_skipped = True
        continue

    processed_row = [float(value) if value else None for value in row]
    processed_data.append(processed_row)
    print(processed_row)

#average seebeck voltages and draw the relationship
data_seebeck = []
seebeck_column_index = 4

for row_index, row in enumerate(data):
    if row_index == 0:
        continue

    try:
        voltage = float(row[seebeck_column_index])
    except (ValueError, TypeError):
        continue

    choice = is_new_angle(processed_data,row_index,1)
    if choice:
        vol_ave = averaged_volatge(processed_data,row_index,seebeck_column_index)

        current_angle = row[7]
        modified_row = [vol_ave,current_angle]
        data_seebeck.append(modified_row)

for row in data_seebeck:
    print(row)

output_file = 'processed_data-0713_seebeck.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_seebeck:
        writer.writerow(row)

print(f"File is written as: {output_file}")

#average nernst voltages and draw the relationship
data_nernst = []
nernst_column_index = 5

for row_index, row in enumerate(data):

    if row_index == 0:
        continue

    try:
        voltage = float(row[nernst_column_index])
    except (ValueError, TypeError):
        continue

    choice = is_new_angle(processed_data,row_index,1)
    if choice:
        vol_ave = averaged_volatge(processed_data,row_index,nernst_column_index)

        current_angle = row[7]
        modified_row = [vol_ave,current_angle]
        data_nernst.append(modified_row)

for row in data_nernst:
    print(row)

output_file = 'processed_data_nernst-0713.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_nernst:
        writer.writerow(row)

print(f"File is written as: {output_file}")