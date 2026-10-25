#!/bin/bash
# Example 06: Create and inspect a COG end-to-end.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INPUT_TIF="$SCRIPT_DIR/data/input.tif"
OUTPUT_DIR="$SCRIPT_DIR/output"
COG_TIF="$OUTPUT_DIR/output_cog.tif"
mkdir -p "$OUTPUT_DIR"

if [[ ! -f "$INPUT_TIF" ]]; then
  echo "Input raster not found: $INPUT_TIF" >&2
  echo "Place a source GeoTIFF at this path before running the workflow." >&2
  exit 2
fi

echo "=== Step 1: Create COG with internal overviews ==="
gdal_translate -of COG -co COMPRESS=DEFLATE -co BIGTIFF=IF_SAFER -co OVERVIEWS=AUTO "$INPUT_TIF" "$COG_TIF"

echo "=== Step 2: Inspect metadata and layout ==="
gdalinfo "$COG_TIF" | grep -E "Driver|Size is|Overviews:|Block=" || true

echo "=== Step 3: Confirm output is readable ==="
gdal_translate -q -of VRT "$COG_TIF" "$OUTPUT_DIR/output_cog.vrt"
gdalinfo "$OUTPUT_DIR/output_cog.vrt" >/dev/null
echo "VRT references the COG and GDAL can read its metadata."

echo "=== Step 4: Serve with TiTiler (optional, requires Docker) ==="
echo "docker run --rm -p 8080:8080 -v "$OUTPUT_DIR:/data:ro" ghcr.io/developmentseed/titiler:latest"
echo "Then open http://localhost:8080/health and consult the TiTiler version's API docs."
echo "Do not assume a local file path is accessible to a remote TiTiler deployment."
ls -lh "$OUTPUT_DIR"
