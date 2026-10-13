#!/bin/bash
# Example 06: Full COG workflow
set -e

INPUT_DIR="$(dirname "$0")/data"
OUTPUT_DIR="$(dirname "$0")/output"
mkdir -p "$OUTPUT_DIR"

echo "=== Step 1: Create COG ==="
gdal_translate -of COG -co COMPRESS=DEFLATE -co BIGTIFF=YES \
  "$INPUT_DIR/input.tif" "$OUTPUT_DIR/output_cog.tif"

echo "=== Step 2: Validate ==="
gdalinfo "$OUTPUT_DIR/output_cog.tif" | grep -E "Driver|Size is"

echo "=== Step 3: Create overviews ==="
gdaladdo -r average "$OUTPUT_DIR/output_cog.tif" 2 4 8 16

echo "=== Step 4: Verify overviews ==="
gdalinfo "$OUTPUT_DIR/output_cog.tif" | grep "Overview"

echo "=== Step 5: Serve with TiTiler ==="
echo "Run: docker run -p 8080:8080 -v $(pwd)/$OUTPUT_DIR:/data developmentseed/titiler:latest"
echo "Then: http://localhost:8080/cog/tiles/{z}/{x}/{y}?url=/data/output_cog.tif"

echo "=== Output ==="
ls -lh "$OUTPUT_DIR/"
