#!/bin/bash
# Example 01: Create Cloud Optimized GeoTIFF with GDAL
set -e

INPUT_DIR="$(dirname "$0")/data"
OUTPUT_DIR="$(dirname "$0")/output"
mkdir -p "$OUTPUT_DIR"

echo "=== Create COG with DEFLATE compression ==="
gdal_translate -of COG -co COMPRESS=DEFLATE -co BIGTIFF=YES \
  "$INPUT_DIR/input.tif" "$OUTPUT_DIR/output_cog.tif"

echo "=== Create COG with ZSTD compression ==="
gdal_translate -of COG -co COMPRESS=ZSTD -co BIGTIFF=YES \
  "$INPUT_DIR/input.tif" "$OUTPUT_DIR/output_zstd.tif"

echo "=== Create COG with internal overview levels ==="
# Use smaller tiles so this 512x512 demo visibly produces internal overview levels.
gdal_translate -of COG -co COMPRESS=DEFLATE -co BLOCKSIZE=128 -co OVERVIEWS=IGNORE_EXISTING \
  "$INPUT_DIR/input.tif" "$OUTPUT_DIR/output_overviews.tif"

echo "=== Verify COG structure ==="
gdalinfo "$OUTPUT_DIR/output_cog.tif" | head -20

echo "=== Output ==="
ls -lh "$OUTPUT_DIR/"
