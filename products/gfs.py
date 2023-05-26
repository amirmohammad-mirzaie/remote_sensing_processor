from typing import List
import numpy as np
import pandas as pd
import rasterio
import geopandas as gpd
from rasterio.mask import mask
from shapely.geometry import mapping


class Landsat(object):

    def __init__(self, file_paths: List[str], shapefile_path: str, classes_column_name: str):
        self.file_paths = file_paths
        self._shapefile_path = shapefile_path
        self.classes_column_name = classes_column_name
        self._shapefile = gpd.read_file(self._shapefile_path)

    @property
    def shapefile_path(self):
        return self._shapefile_path

    @shapefile_path.setter
    def shapefile_path(self, value):
        self._shapefile_path = value
        self._shapefile = gpd.read_file(self._shapefile_path)

    def extract_data_by_multiple_polygons(self):
        """
        method used to extract data from multiple landsat bands and convert them into a pandas dataframe.
        """
        this_band_df = []

        for j, band in enumerate(self.file_paths):
            src = rasterio.open(band)

            geoms = self._shapefile.geometry.values
            classes = self._shapefile[self.classes_column_name].values

            geoms = [[mapping(geoms[i])] for i in range(len(geoms))]

            dfs = []

            for i, geom in enumerate(geoms):

                out_image, out_transform = mask(src, geoms[i], crop=True)
                no_data = src.nodata
                data = out_image[0]

                elev = np.extract(data != no_data, data)

                df = pd.DataFrame({self.file_paths[j]: elev})

                if j == 0:
                    df[self.classes_column_name] = classes[i]

                dfs.append(df)

            this_band_df.append(pd.concat(dfs))

        final_df = pd.concat(this_band_df, axis=1)
        return final_df
