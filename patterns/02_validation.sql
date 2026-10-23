-- Pattern 02: COG Validation
-- Validate COG structure and tiling
-- gdalinfo output_cog.tif

-- Check for internal tiling
-- gdalinfo -json output_cog.tif | jq '.bands[0].blockSize'

-- Verify overview levels
-- gdalinfo -json output_cog.tif | jq '.overviews'
