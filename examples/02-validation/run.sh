#!/bin/bash
# Example 02: Validate Cloud Optimized GeoTIFF
set -e

INPUT_DIR="$(dirname "$0")/data"
OUTPUT_DIR="$(dirname "$0")/output"
mkdir -p "$OUTPUT_DIR"

echo "=== Validate COG structure ==="
gdalinfo "$INPUT_DIR/input.tif" | grep -E "Driver|Size is|Origin is|Pixel Size|Metadata"

echo "=== Check for COG-specific features ==="
gdalinfo "$INPUT_DIR/input.tif" | grep -i "cloud optimized" || echo "Not a COG"

echo "=== Validate with gdalinfo JSON ==="
gdalinfo -json "$INPUT_DIR/input.tif" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Driver: {data.get(\"driverShortName\", \"unknown\")}')
print(f'Size: {data.get(\"size\", [])}')
print(f'CRS: {data.get(\"coordinateSystem\", {}).get(\"wkt\", \"unknown\")[:50]}...')
"

echo "=== Compare file sizes ==="
ls -lh "$INPUT_DIR/input.tif" "$OUTPUT_DIR/output_cog.tif"
