# Pixel Aggregation

To better represent AquaCrop model mechanics and improve visualization, validation metrics are computed on aggregated CGLS validation 
pixels. As resampling is relatively simple using tools like NCO, the following assets are provided to process validation datasets
only in areas corresponding to crop locations. The following describes the relative procedures:

1. Mask Out Regions
   - The crop maps described in this study already includes resampling to the resolution of the CGLS DMP and FCOVER grids (300m)
   - Using the maps, pixels not corresponding to crop specific locations are masked out
   - Python script: **insert .py file here**

2. Resampling using NCO
   - The masked data will convert non-crop pixel validation cells to NaN values.
   - Resampling can be run on the entire file, and only CGLS signals over crop specific locations are aggregated.
   - NCO command: **ncremap -i masked_output.nc -o resampled_output.nc -d destination_grid.nc**
