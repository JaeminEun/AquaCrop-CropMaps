# Crop Map Intersection for AquaCrop Simulations

This project involves combining crop maps from multiple sources and years to generate stable, location-specific masks for AquaCrop simulations. The goal is to ensure that AquaCrop is evaluated only in regions where a particular crop type (e.g., maize, spring cereals, winter cereals) consistently exists across multiple years, reducing the confounding influence of crop rotation or land use change.

## 📦 Datasets Used

The crop type information used in this analysis is derived from publicly available remote sensing-based land cover products:

1. **EUCROPMAP 2018**  
   - Source: Joint Research Centre (JRC), European Commission  
   - URL: [https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EUCROPMAP/2018/](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EUCROPMAP/2018/)  
   - Description: EUCROPMAP provides annual crop-specific land cover maps at 10-meter resolution across the European Union. It distinguishes a wide variety of crop types based on Sentinel-1 and Sentinel-2 data.

2. **WorldCereal 2021**  
   - Source: ESA WorldCereal project  
   - DOI: [10.5281/zenodo.7875105](https://zenodo.org/records/7875105)  
   - Description: A global, open-source dataset providing cropland extent and crop type information (cereal vs. maize) at 10-meter resolution using seasonal Sentinel data. Note that cereal types (wheat, barley, rye) are not distinguished due to spectral similarity.

3. **EUCROPMAP 2022**  
   - Source: Joint Research Centre (JRC), European Commission  
   - URL: [https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EUCROPMAP/2022/EU_CropMap_22_v1_stratum_EU27-HR.tif](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EUCROPMAP/2022/EU_CropMap_22_v1_stratum_EU27-HR.tif)  
   - Description: Updated EUCROPMAP product offering crop-specific classifications for 2022. Used similarly to the 2018 dataset.

## 🧩 Methodology

The datasets above are harmonized and combined through the following steps:

1. **Crop Type Selection**  
   - The analysis focuses on three crop classes: **maize**, **spring cereals**, and **winter cereals**.
   - For **spring and winter cereals**, these are used as proxies for **wheat**, acknowledging that WorldCereal does not distinguish between wheat, barley, and rye.

2. **Spatial Intersection**  
   - The goal is to identify stable locations for each crop type — places where the same crop is present in all three datasets (2018, 2021, and 2022).
   - This helps avoid the confounding effect of crop rotation or inconsistent labeling between years.

3. **Resampling**  
   - The final intersected crop masks are resampled using **nearest-neighbor interpolation** to match the resolution of the Copernicus Global Land Service (CGLS) observations (300 meters).
   - These observations are then used to evaluate the AquaCrop simulations.

## 📈 Application

These stable, crop-specific location masks are used to evaluate **multi-year AquaCrop simulations**, ensuring that the comparison is consistent and only involves areas where crop classification remains unchanged over time. This improves the robustness and interpretability of the model evaluation.
