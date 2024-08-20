#file_path = "2024_06_06_thermal_conductivity_8.0K_110u.dat"

#with open(file_path, 'r') as file:
#    for line in file:
#       print(line.strip());

#the data file given is CSV file.

def is_low_voltage(voltage, threshold):
    return voltage is not None and voltage < threshold

def is_high_voltage(voltage, threshold):
    return voltage is not None and voltage > threshold

def is_jump_point(data, row_index, jump_threshold):
    if row_index < 5:
        return False

    current_value = data[row_index][4]
    if current_value is None:
        return False

    current_value = abs(float(current_value))
    previous_values = [data[i][4] for i in range(row_index - 5, row_index) if data[i][4] is not None]

    if len(previous_values) < 5:
        return False

    previous_values = [abs(float(value)) for value in previous_values]
    for previous_value in previous_values:
        if abs(current_value-previous_value) < jump_threshold:
            return True

def is_new_angle(data, row_index, jump_threshold=1.0):
    if row_index < 0 or row_index >= len(data):
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
    choiceC = False
    while row_index < len(data):
        choiceD = True if data[row_index][column_index] is not None else False

        if not choiceC and choiceD:
            try:
                selected_data.append(float(data[row_index][column_index]))
            except ValueError:
                pass
        if choiceC is not None:
            pass
        if choiceC:
            break

        row_index += 1
        choiceC = is_new_angle(data, row_index, jump_threshold=1.0)


    if selected_data:
        vol_ave = sum(selected_data) / len(selected_data)
    else:
        vol_ave = 0

    return vol_ave

#########################################
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


#Select and Average low voltages. Modify seebeck voltage data.
data_withoutOffset = []

for row_index, row in enumerate(data):
    if len(row) < 8 or row[4] is None:
        continue

    try:
        voltage = float(row[4])
    except ValueError:
        continue

    choice = is_low_voltage(abs(float(row[4])), 4e-7)
    if choice:
        modified_row = row[:]
        modified_row[4] = 0
        data_withoutOffset.append(modified_row)
    else:
        sum_low = 0
        count = 0
        i = 1

        while count < 40:
            if row_index - i >= 0 and len(data[row_index - i]) >= 8 and data[row_index - i][4] is not None:
                try:
                    neighbor_voltage = float(data[row_index - i][4])
                    if is_low_voltage(abs(neighbor_voltage), 4e-7):
                        sum_low += neighbor_voltage
                        count += 1
                except ValueError:
                    pass

            if row_index + i < len(data) and len(data[row_index + i]) >= 8 and data[row_index + i][4] is not None:
                try:
                    neighbor_voltage = float(data[row_index + i][4])
                    if is_low_voltage(abs(neighbor_voltage), 4e-7):
                        sum_low += neighbor_voltage
                        count += 1
                except ValueError:
                    pass

            i += 1

        ave_low = sum_low / count if count > 0 else 0
        modified_row = row[:]
        modified_row[4] = float(row[4]) - ave_low
        data_withoutOffset.append(modified_row)

for row in data_withoutOffset:
    print(row)

output_file = 'processed_data-0713-seebeck.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_withoutOffset:
        writer.writerow(row)

print(f"File is written as: {output_file}")

##################################################
#Select the On Voltage
data_On = []

for row_index, row in enumerate(data_withoutOffset):
    if len(row) < 5 or row[4] is None:
        continue

    try:
        voltage = float(row[4])
    except ValueError:
        continue

    choiceA = is_high_voltage(abs(float(row[4])), 1e-6)
    choiceB = is_jump_point(data_withoutOffset,row_index,5e-7)

    if choiceA and choiceB:
        modified_row = row[:]
        modified_row[4] = row[4]
        data_On.append(modified_row)
    else:
        modified_row = row[:]
        modified_row[4] = None
        data_On.append(modified_row)

for row in data_On:
    print(row)

output_file = 'processed_ONdata-07013-seebeck.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_On:
        writer.writerow(row)

print(f"File is written as: {output_file}")

###############################################
#average seebeck voltages for each angle
data_seebeck = []
seebeck_column_index = 4

for row_index, row in enumerate(data_On):
    choice = is_new_angle(data_On,row_index,1)
    if choice:
        vol_ave = averaged_volatge(data_On,row_index,seebeck_column_index)

        current_angle = row[7]
        modified_row = [vol_ave,current_angle]
        data_seebeck.append(modified_row)

for row in data_seebeck:
    print(row)

output_file = 'Result-0713_seebeck.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_seebeck:
        writer.writerow(row)

print(f"File is written as: {output_file}")

#seebeck voltage done

######################
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


#Select and Average low voltages. Modify seebeck voltage data.
data_withoutOffset = []

for row_index, row in enumerate(data):
    if len(row) < 8 or row[5] is None:
        continue

    try:
        voltage = float(row[5])
    except ValueError:
        continue

    choice = is_low_voltage(abs(float(row[5])), 4e-7)
    if choice:
        modified_row = row[:]
        modified_row[5] = 0
        data_withoutOffset.append(modified_row)
    else:
        sum_low = 0
        count = 0
        i = 1

        while count < 40:
            if row_index - i >= 0 and len(data[row_index - i]) >= 8 and data[row_index - i][5] is not None:
                try:
                    neighbor_voltage = float(data[row_index - i][5])
                    if is_low_voltage(abs(neighbor_voltage), 8e-7):
                        sum_low += neighbor_voltage
                        count += 1
                except ValueError:
                    pass

            if row_index + i < len(data) and len(data[row_index + i]) >= 8 and data[row_index + i][5] is not None:
                try:
                    neighbor_voltage = float(data[row_index + i][5])
                    if is_low_voltage(abs(neighbor_voltage), 8e-7):
                        sum_low += neighbor_voltage
                        count += 1
                except ValueError:
                    pass

            i += 1

        ave_low = sum_low / count if count > 0 else 0
        modified_row = row[:]
        modified_row[5] = float(row[5]) - ave_low
        data_withoutOffset.append(modified_row)

for row in data_withoutOffset:
    print(row)

output_file = 'processed_data-0713-nernst.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_withoutOffset:
        writer.writerow(row)

print(f"File is written as: {output_file}")

##################################################
#Select the On Voltage
data_On = []

for row_index, row in enumerate(data_withoutOffset):
    if len(row) < 5 or row[5] is None:
        continue

    try:
        voltage = float(row[5])
    except ValueError:
        continue

    choiceA = is_high_voltage(abs(float(row[5])), 9e-6)
    choiceB = is_jump_point(data_withoutOffset,row_index,9e-7)

    if choiceA and choiceB:
        modified_row = row[:]
        modified_row[5] = row[5]
        data_On.append(modified_row)
    else:
        modified_row = row[:]
        modified_row[5] = None
        data_On.append(modified_row)

for row in data_On:
    print(row)

output_file = 'processed_ONdata-07013-nernst.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_On:
        writer.writerow(row)

print(f"File is written as: {output_file}")

###############################################
#average seebeck voltages for each angle
data_seebeck = []
seebeck_column_index = 5

for row_index, row in enumerate(data_On):
    choice = is_new_angle(data_On,row_index,1)
    if choice:
        vol_ave = averaged_volatge(data_On,row_index,seebeck_column_index)

        current_angle = row[7]
        modified_row = [vol_ave,current_angle]
        data_seebeck.append(modified_row)

for row in data_seebeck:
    print(row)

output_file = 'Result-0713_nernst.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_seebeck:
        writer.writerow(row)

print(f"File is written as: {output_file}")