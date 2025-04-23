# Jaemin Eun

import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Define file paths
nc_files = {
    "CC": {
        "R": ["/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/Metrics/CC/Map_CC_R.nc",
               "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/Metrics/CC/Map_CC_R.nc",
               "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/Metrics/CC/Map_CC_R.nc",
               "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/Metrics/CC/Map_CC_R.nc"],
        "Bias": ["/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/Metrics/CC/Map_CC_Bias.nc",
                "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/Metrics/CC/Map_CC_Bias.nc",
                "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/Metrics/CC/Map_CC_Bias.nc",
                "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/Metrics/CC/Map_CC_Bias.nc"],
        "RMSD": ["/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/Metrics/CC/Map_CC_RMSD.nc",
                 "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/Metrics/CC/Map_CC_RMSD.nc",
                 "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/Metrics/CC/Map_CC_RMSD.nc",
                 "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/Metrics/CC/Map_CC_RMSD.nc"],
        "ubRMSD": ["/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/Metrics/CC/Map_CC_ubRMSD.nc",
                   "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/Metrics/CC/Map_CC_ubRMSD.nc",
                   "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/Metrics/CC/Map_CC_ubRMSD.nc",
                   "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/Metrics/CC/Map_CC_ubRMSD.nc"]
    },
    "Biomass": {
        "R": ["/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/Metrics/Biomass/Map_Biomass_R.nc",
               "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/Metrics/Biomass/Map_Biomass_R.nc",
               "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/Metrics/Biomass/Map_Biomass_R.nc",
               "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/Metrics/Biomass/Map_Biomass_R.nc"],
        "Bias": ["/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/Metrics/Biomass/Map_Biomass_Bias.nc",
                 "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/Metrics/Biomass/Map_Biomass_Bias.nc",
                 "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/Metrics/Biomass/Map_Biomass_Bias.nc",
                 "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/Metrics/Biomass/Map_Biomass_Bias.nc"],
        "RMSD": ["/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/Metrics/Biomass/Map_Biomass_RMSD.nc",
                 "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/Metrics/Biomass/Map_Biomass_RMSD.nc",
                 "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/Metrics/Biomass/Map_Biomass_RMSD.nc",
                 "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/Metrics/Biomass/Map_Biomass_RMSD.nc"],
        "ubRMSD": ["/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/Metrics/Biomass/Map_Biomass_ubRMSD.nc",
                   "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/Metrics/Biomass/Map_Biomass_ubRMSD.nc",
                   "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/Metrics/Biomass/Map_Biomass_ubRMSD.nc",
                   "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/Metrics/Biomass/Map_Biomass_ubRMSD.nc"]
    }
}

crop_labels = ["Gen Cal", "Gen GDD", "Maize Cal", "Maize GDD"]
crop_colors = ["grey", "darkgreen", "gold", "tab:brown"]
metrics = ["R", "Bias", "RMSD", "ubRMSD"]

# Create subplots
fig, axes = plt.subplots(2, len(metrics), figsize=(16, 8))
axes[0, 2].sharey(axes[0, 3])  # Share y-axis for CC RMSD and CC ubRMSD
axes[1, 2].sharey(axes[1, 3])  # Share y-axis for Biomass RMSD and Biomass ubRMSD
axes[0, 0].sharey(axes[1,0 ])  # Share y-axis for CC R and Biomass R

axes[0,0].set_ylabel('Correlation')
axes[1,0].set_ylabel('Correlation')
axes[0,1].set_ylabel('Bias')
axes[1,1].set_ylabel('Bias (kg ha$^{-1}$ day$^{-1}$)')
axes[0,2].set_ylabel('RMSD')
axes[1,2].set_ylabel('RMSD (kg ha$^{-1}$ day$^{-1}$)')
axes[0,3].set_ylabel('ubRMSD')
axes[1,3].set_ylabel('ubRMSD (kg ha$^{-1}$ day$^{-1}$)')

for row, category in enumerate(["CC", "Biomass"]):
    for col, metric in enumerate(metrics):
        data = []
        for i, file in enumerate(nc_files[category][metric]):
            ds = xr.open_dataset(file)
            var_name = list(ds.data_vars.keys())[0]
            values = ds[var_name].values.flatten()
            values = values[~np.isnan(values)]
            data.append(values)
        
        sns.boxplot(data=data, ax=axes[row, col], palette=crop_colors)
        #axes[row, col].set_title(f"{category} - {metric}", fontsize=16)
        axes[row, col].set_xticklabels(crop_labels)
        axes[row, col].tick_params(axis='y', labelsize=12)  # Increase y-axis label font size
        #axes[row, col].tick_params(axis='x', labelsize=11)  # Increase y-axis label font size
        axes[row, col].set_title(f"{category} - {metric}", fontsize=16)
        axes[row, col].grid(True)
        
plt.tight_layout()
plt.savefig('Boxplots.png', dpi=400)
plt.show()



