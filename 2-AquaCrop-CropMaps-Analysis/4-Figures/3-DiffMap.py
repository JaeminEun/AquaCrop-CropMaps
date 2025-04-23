# Jaemin Eun

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as mcolors

# Load netCDF data
file1 = "GenDiff.nc"
file2 = "MaizeDiff.nc"

ds1 = xr.open_dataset(file1)
ds2 = xr.open_dataset(file2)

# Assuming the variables of interest are named 'var' and coordinates are 'lat' and 'lon'
var1 = ds1["correlation"]
var2 = ds2["correlation"]
lats = ds1["lat"].values
lons = ds1["lon"].values

# Define figure and axes
fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
fig.suptitle("Correlation Difference (GDD - Calendar)", fontsize=14, fontweight='bold')

# Define fixed color scale range
vmin, vmax = -0.4, 0.4

# Function to plot each map with a specified colormap
def plot_map(ax, data, title, cmap, label):
    m = Basemap(projection="cyl", llcrnrlon=lons.min(), urcrnrlon=lons.max(),
                llcrnrlat=lats.min(), urcrnrlat=lats.max(), resolution="i", ax=ax)
    
    m.drawcoastlines()
    m.drawcountries()
    m.drawmeridians([0, 20], labels=[0, 0, 0, 1])
    m.drawparallels([45, 55], labels=[1, 0, 0, 0])

    lon_grid, lat_grid = np.meshgrid(lons, lats)
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax, clip=False)
    sc = m.pcolormesh(lon_grid, lat_grid, data, cmap=cmap, norm=norm)
    cbar = fig.colorbar(sc, ax=ax, orientation="horizontal", pad=0.05, extend='both')
    cbar.set_label("Correlation Difference")

    # Compute statistics
    mean_val = np.nanmean(data)
    std_val = np.nanstd(data)
    
    # Add statistics box at the top left corner
    textstr = f'Mean: {mean_val:.3f}\nStd: {std_val:.2f}'
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    # Add subplot label outside the main map (top-left corner of figure)
    ax.annotate(label, xy=(-0.1, 1.05), xycoords='axes fraction', fontsize=12, fontweight='bold',
                verticalalignment='top', horizontalalignment='left')
    
    ax.set_title(title)

# Plot both datasets with different colormaps
plot_map(axes[0], var1, "Generic Crop", "BrBG", "a)")
plot_map(axes[1], var2, "Maize", "PiYG", "b)")

plt.savefig("CorrelationDiff.png", dpi=400)
plt.show()

