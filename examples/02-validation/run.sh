#!/bin/bash
# Example 02: Inspect and validate a Cloud Optimized GeoTIFF
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INPUT_DIR="$SCRIPT_DIR/data"
INPUT_TIF="${COG_FILE:-$INPUT_DIR/input.tif}"
OUTPUT_DIR="$SCRIPT_DIR/output"
mkdir -p "$OUTPUT_DIR"

if [[ ! -f "$INPUT_TIF" ]]; then
  echo "Input raster not found: $INPUT_TIF" >&2
  echo "Set COG_FILE=/path/to/raster.tif or place input.tif in $INPUT_DIR." >&2
  exit 2
fi

echo "=== Inspect raster metadata ==="
gdalinfo "$INPUT_TIF" | grep -E "Driver|Size is|Origin is|Pixel Size|Metadata" || true

echo "=== Inspect COG layout metadata ==="
gdalinfo "$INPUT_TIF" | grep -i "cloud optimized" || echo "GDAL did not report explicit COG layout metadata; inspect block layout and overviews below."

echo "=== Parse GDAL JSON metadata ==="
gdalinfo -json "$INPUT_TIF" | python3 -c '
import json, sys
data = json.load(sys.stdin)
print(f"Driver: {data.get('driverShortName', 'unknown')}")
print(f"Size: {data.get('size', [])}")
print(f"CRS present: {bool(data.get('coordinateSystem', {}).get('wkt'))}")
print(f"Band count: {len(data.get('bands', []))}")
'

echo "=== File and overview summary ==="
ls -lh "$INPUT_TIF"
gdalinfo "$INPUT_TIF" | grep -E "Overviews:|Block=" || true
