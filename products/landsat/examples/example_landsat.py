from os.path import join

from products.landsat.landsat import Landsat
import os

from settings import ROOT_DIR

print(os.getcwd())
if __name__ == '__main__':
    landsat_file_band_list = [
        join(ROOT_DIR, 'products/landsat/examples/sample_data/raster_data/sample_LE07_L2SP_165035_20020528_20200916_02_T1_ST_B1.tif'),
        join(ROOT_DIR, 'products/landsat/examples/sample_data/raster_data/sample_LE07_L2SP_165035_20020528_20200916_02_T1_ST_B2.tif'),
    ]
    shapefile_path = join(ROOT_DIR, 'products/landsat/examples/sample_data/vector_data/polygons.shp')

    a = Landsat(file_paths=landsat_file_band_list, shapefile_path=shapefile_path, classes_column_name="id")
    b = a.extract_data_by_multiple_polygons()

