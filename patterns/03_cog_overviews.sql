-- Pattern 03: COG Overviews
-- Inspect overview levels in a COG
-- gdalinfo -json output_cog.tif | jq '.overviews'

-- Build overviews explicitly (GDAL OVR) for non-COG GeoTIFFs
-- gdaladdo input.tif 2 4 8 16

-- Create COG with explicit overview levels
-- gdal_translate -of COG -co COMPRESS=DEFLATE -co OVERVIEWS=IGNORE_EXISTING input.tif output_overviews.tif

-- Verify overview resolution and block sizes
-- gdalinfo -json output_cog.tif | jq '{overviews, blockSize: .bands[0].blockSize}'
