#file_path = "2024_06_06_thermal_conductivity_8.0K_110u.dat"

#with open(file_path, 'r') as file:
#    for line in file:
#       print(line.strip());

#the data file given is CSV file.

def is_low_voltage(voltage, threshold):
    return voltage is not None and voltage < threshold

def is_high_voltage(voltage, threshold):
    return voltage is not None and voltage > threshold

'''def average_low_voltage_near_peaks(data, voltage_column_index, high_threshold, low_threshold, range_size):
    low_voltage_averages = []

    for i in range(len(data)):
        voltage = data[i][voltage_column_index]

        if is_high_voltage(voltage, high_threshold):
            # Define the range around the peak
            start_index = max(0, i - range_size)
            end_index = min(len(data), i + range_size + 1)

            # Extract low voltages in the range
            low_voltages = [data[j][voltage_column_index] for j in range(start_index, end_index)
                            if is_low_voltage(data[j][voltage_column_index], low_threshold)]

           # Calculate the average of the low voltages in the range
            if low_voltages:
                low_voltage_averages.append(sum(low_voltages) / len(low_voltages))

# Return the list of averages or None if no low voltages were found
    if low_voltage_averages:
       return low_voltage_averages
    return None'''


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


import csv
file_path = "2024_06_06_thermal_conductivity_8.0K_110u.dat"

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


#Select and Average low voltages. Modify voltage data.
data_withoutOffset = []

for row_index, row in enumerate(data):
    if len(row) < 5 or row[4] is None:
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
            if row_index - i >= 0 and len(data[row_index - i]) >= 5 and data[row_index - i][4] is not None:
                try:
                    neighbor_voltage = abs(float(data[row_index - i][4]))
                    if is_low_voltage(neighbor_voltage, 4e-7):
                        sum_low += neighbor_voltage
                        count += 1
                except ValueError:
                    pass

            if row_index + i < len(data) and len(data[row_index + i]) >= 5 and data[row_index + i][4] is not None:
                try:
                    neighbor_voltage = abs(float(data[row_index + i][4]))
                    if is_low_voltage(neighbor_voltage, 4e-7):
                        sum_low += neighbor_voltage
                        count += 1
                except ValueError:
                    pass

            i += 1

        ave_low = sum_low / count if count > 0 else 0
        modified_row = row[:]
        modified_row[4] = abs(float(row[4])) - ave_low
        data_withoutOffset.append(modified_row)

for row in data_withoutOffset:
    print(row)

output_file = 'processed_data-0606.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_withoutOffset:
        writer.writerow(row)

print(f"File is written as: {output_file}")


#Select the On Voltage
data_On = []

for row_index, row in enumerate(data_withoutOffset):
    if len(row) < 5 or row[4] is None:
        continue

    try:
        voltage = float(row[4])
    except ValueError:
        continue

    choiceA = is_high_voltage(abs(float(row[4])), 1.9e-6)
    choiceB = is_jump_point(data_withoutOffset,row_index,0.05e-6)

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

output_file = 'processed_ONdata-0606.csv'

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in data_On:
        writer.writerow(row)

print(f"File is written as: {output_file}")
