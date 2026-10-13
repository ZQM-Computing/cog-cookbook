#!/bin/bash
# Example 05: COG performance comparison
set -e

INPUT_DIR="$(dirname "$0")/data"
OUTPUT_DIR="$(dirname "$0")/output"

echo "=== File size comparison ==="
echo "Original TIFF:"
ls -lh "$INPUT_DIR/input.tif"
echo ""
echo "Cloud Optimized GeoTIFF:"
ls -lh "$OUTPUT_DIR/output_cog.tif"
echo ""

echo "=== Read performance: full raster ==="
echo "Original:"
time gdal_translate -of GTiff "$INPUT_DIR/input.tif" /dev/null
echo ""
echo "COG:"
time gdal_translate -of GTiff "$OUTPUT_DIR/output_cog.tif" /dev/null
echo ""

echo "=== Read performance: subset (10% of raster) ==="
echo "Original (reads full file):"
time gdal_translate -of GTiff -projwin -80.93 29.03 -80.92 29.02 "$INPUT_DIR/input.tif" /dev/null
echo ""
echo "COG (reads only required tiles):"
time gdal_translate -of GTiff -projwin -80.93 29.03 -80.92 29.02 "$OUTPUT_DIR/output_cog.tif" /dev/null
