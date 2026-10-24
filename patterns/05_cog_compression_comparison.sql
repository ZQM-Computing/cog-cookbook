-- Pattern 05: COG Compression Comparison
-- Compare file sizes across compression algorithms
-- ls -lh output_cog.tif output_zstd.tif output_lzw.tif

-- Create COG with LZW compression
-- gdal_translate -of COG -co COMPRESS=LZW -co BIGTIFF=YES input.tif output_lzw.tif

-- Create COG with DEFLATE compression (predictor=2 for integer data)
-- gdal_translate -of COG -co COMPRESS=DEFLATE -co PREDICTOR=2 input.tif output_deflate_pred.tif

-- Benchmark read throughput per compression
-- gdalinfo -stats output_cog.tif
