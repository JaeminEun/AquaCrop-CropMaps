import os
from datetime import datetime

# Directory containing the files
directory = 'ReplacePathYourDirectory'  # Replace with the path to your directory

# List to hold the number of days since 1970-01-01
days_since_epoch = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.nc'):  # Check if the file has a .nc extension
        parts = filename.split('_')
        if len(parts) > 3:
            date_part = parts[3]
            if len(date_part) >= 8:
                date_str = date_part[:8]
                date_obj = datetime.strptime(date_str, '%Y%m%d')
                epoch = datetime(1970, 1, 1)
                days_diff = (date_obj - epoch).days
                days_since_epoch.append(days_diff)

days_since_epoch_sorted = sorted(days_since_epoch)
#print(days_since_epoch_sorted)

# Output file to save the results
output_file = 'output_days.txt'  # Replace with your desired output file name

# Write the results to the output file
with open(output_file, 'w') as f:
    f.write(','.join(map(str, days_since_epoch_sorted)))

