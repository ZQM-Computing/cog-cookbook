-- Pattern 04: COG Tiling
-- Inspect internal tile (block) layout
-- gdalinfo -json output_cog.tif | jq '.bands[0].blockSize'

-- Create COG with custom tile size
-- gdal_translate -of COG -co COMPRESS=DEFLATE -co BLOCKSIZE=512 input.tif output_tiled_512.tif

-- Create COG with 256x256 tiles (default for COG)
-- gdal_translate -of COG -co COMPRESS=ZSTD -co BLOCKSIZE=256 input.tif output_tiled_256.tif

-- Check IFD (Image File Directory) count and structure
-- gdalinfo -json output_cog.tif | jq '{size, overviews}'
