-- Pattern 01: COG Creation
-- Create Cloud Optimized GeoTIFF with DEFLATE compression
-- gdal_translate -of COG -co COMPRESS=DEFLATE -co BIGTIFF=YES input.tif output_cog.tif

-- Create COG with ZSTD compression
-- gdal_translate -of COG -co COMPRESS=ZSTD -co BIGTIFF=YES input.tif output_zstd.tif

-- Create COG with overview levels
-- gdal_translate -of COG -co COMPRESS=DEFLATE -co OVERVIEWS=AUTO input.tif output_overviews.tif
