#!/bin/bash

# Load the NCO module
module load NCO/5.0.1-foss-2021a

# Input directory containing .nc files
input_dir="INPUT_DIR"

# Output directory to save modified .nc files
output_dir="OUTPUT_DIR"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through each .nc file in the input directory
for file in "$input_dir"/*.nc; do
    # Extract filename without extension
    filename=$(basename "$file" .nc)
    
    # Run ncks command on the current file and save output to the output directory
    ncks -d lat,35.,59. -d lon,-9.,35. "$file" "$output_dir"/"$filename"_SUBSET.nc
    
    echo "Processed $file"
done

echo "All files processed."

