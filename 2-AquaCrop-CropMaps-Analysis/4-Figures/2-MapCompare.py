# Jaemin Eun

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors

# File paths
nc_CC_R_GenCal_path = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/Metrics/CC/Map_CC_R.nc'
nc_CC_R_GenGDD_path = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/Metrics/CC/Map_CC_R.nc'
nc_CC_R_MzCal_path  = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/Metrics/CC/Map_CC_R.nc'
nc_CC_R_MzGDD_path  = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/Metrics/CC/Map_CC_R.nc'

# List of files and corresponding titles for the subplots
file_paths = [nc_CC_R_GenCal_path, nc_CC_R_GenGDD_path, nc_CC_R_MzCal_path, nc_CC_R_MzGDD_path]
titles     = ['Generic - Calendar', 'Generic - GDD', 'Maize - Calendar', 'Maize - GDD']

# ------------------------------------------------------------------
# Step 1: Pre-compute global min and max for the correlation data
# ------------------------------------------------------------------
global_min = np.inf
global_max = -np.inf

for file_path in file_paths:
    ds = netCDF4.Dataset(file_path)
    data = ds.variables['correlation'][:]  # adjust variable name if needed
    # Compute min and max while ignoring NaNs if any are present
    global_min = min(global_min, np.nanmin(data))
    global_max = max(global_max, np.nanmax(data))
    ds.close()

# For a diverging colormap centered on 0, force symmetric limits.
abs_max = max(abs(global_min), abs(global_max))
vmin = -abs_max
vmax = abs_max

# ------------------------------------------------------------------
# Step 2: Define discrete color bins with 7 bins, with a custom colormap.
# ------------------------------------------------------------------
nbins = 7
# Create boundaries for 7 bins; 8 boundaries that are symmetric about 0.
bounds = np.array([-0.3, -0.1, 0.1, 0.3, 0.5, 0.6, 0.7, vmax])

# Define a custom colormap:
colors_list = ['#2166ac',  # Single blue for negative values
               'lightgrey',  # Neutral values around 0
               '#ffffb2',  # Light yellow
               '#feb24c',  # Orange-yellow
               '#fd8d3c',  # Deeper orange
               '#f03b20',  # Red-orange
               '#bd0026']  # Dark red
custom_cmap = colors.ListedColormap(colors_list, name='custom_diverging', N=nbins)
norm = colors.BoundaryNorm(bounds, ncolors=nbins)

# Define tick locations at the midpoint of each bin
tick_locs = (bounds[:-1] + bounds[1:]) / 2.0

# ------------------------------------------------------------------
# Step 3: Create a 2x2 subplot figure and plot each map.
# ------------------------------------------------------------------
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 8))
axes = axes.flatten()  # Flatten for easier iteration

# List of subplot labels
subplot_labels = ['a)', 'b)', 'c)', 'd)']

for idx, (file_path, title) in enumerate(zip(file_paths, titles)):
    # Open the NetCDF file and extract data
    ds = netCDF4.Dataset(file_path)
    lats = ds.variables['lat'][:]         # Adjust variable name if needed
    lons = ds.variables['lon'][:]         # Adjust variable name if needed
    data = ds.variables['correlation'][:]      # Adjust variable name if needed
    ds.close()

    # Create 2D coordinate arrays if lats and lons are 1D.
    lon2d, lat2d = np.meshgrid(lons, lats)

    # Create a Basemap instance for this subplot.
    ax = axes[idx]
    m = Basemap(projection='cyl', resolution='i',
                llcrnrlat=np.min(lats), urcrnrlat=np.max(lats),
                llcrnrlon=np.min(lons), urcrnrlon=np.max(lons),
                ax=ax)

    # Draw map features
    m.drawcoastlines()
    m.drawcountries()
    m.drawmeridians([0, 20], labels=[0, 0, 0, 1])
    # Draw parallels at 40° and 50°.
    m.drawparallels([45, 55], labels=[1, 0, 0, 0])

    # Project coordinates and plot the data with the discrete colormap
    x, y = m(lon2d, lat2d)
    cs = m.pcolormesh(x, y, data, cmap=custom_cmap, norm=norm)

    # Calculate and add a transparent text box with statistics.
    mean_val = np.nanmean(data)
    std_val  = np.nanstd(data)
    stats_text = f'Mean: {mean_val:.2f}\nStd: {std_val:.2f}'
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

    # Set the subplot title.
    ax.set_title(title, fontsize=16)

    # Add the subplot label further to the upper left.
    ax.text(-0.05, 1.05, subplot_labels[idx],
            transform=ax.transAxes, fontsize=16, fontweight='bold',
            va='top', ha='left', color='black', clip_on=False)

# ------------------------------------------------------------------
# Step 4: Create a unified colorbar on the right side of the figure.
# ------------------------------------------------------------------
# Increase the pad value to move the colorbar further from the maps.
cbar = fig.colorbar(cs, ax=axes.ravel().tolist(), orientation='vertical',
                    fraction=0.03, pad=0.10, ticks=tick_locs, format='%.1f', extend='both')
# Increase the fontsize for the tick labels and the colorbar label.
cbar.ax.tick_params(labelsize=14)
cbar.set_label('Correlation coefficient', fontsize=12,fontweight='bold', labelpad=20)

# Adjust the layout to leave space for the colorbar.
plt.tight_layout(rect=[0, 0, 0.85, 1])
# Save the figure with 400 dpi.
fig.savefig('CC_R_Comparison.png', dpi=400)
plt.show()
