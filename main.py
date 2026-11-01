import os
import logging
import geopandas as gpd
import pandas as pd
from shapely.validation import make_valid
from sqlalchemy import create_engine, text

# Set up logging for processed, inserted, and failed counts
logging.basicConfig(level=logging.INFO)

# Load mocked test fixture
df = pd.read_csv('mock_data.csv')
logging.info(f"Loaded {len(df)} rows from source.")

# Convert to GeoDataFrame
# Note: Adjust 'x' and 'y' to match the actual Destatis column names
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y), crs="EPSG:3035")

# Reproject to mandatory EPSG:25832 (ETRS89/UTM Zone 32N)
gdf = gdf.to_crs(epsg=25832)

# Validate geometries and handle invalid/empty features
gdf['geometry'] = gdf['geometry'].apply(lambda geom: make_valid(geom) if not geom.is_valid else geom)
gdf = gdf[~gdf['geometry'].is_empty & gdf['geometry'].is_valid]
logging.info(f"{len(gdf)} valid geometries prepared for database insertion.")
