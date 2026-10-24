-- Pattern 06: COG Metadata Extraction
-- Extract full metadata as JSON
-- gdalinfo -json output_cog.tif

-- Extract CRS / coordinate system
-- gdalinfo -json output_cog.tif | jq '.coordinateSystem.wkt'

-- Extract geographic bounds
-- gdalinfo -json output_cog.tif | jq '.cornerCoordinates'

-- Extract band statistics
-- gdalinfo -json output_cog.tif | jq '.bands[].statistics'

-- Extract tags / metadata
-- gdalinfo -json output_cog.tif | jq '.metadata'
