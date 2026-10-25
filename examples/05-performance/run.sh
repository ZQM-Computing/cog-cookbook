#!/bin/bash
# Example 05: Compare local full-raster and windowed reads.
# Timings are illustrative only: OS cache, storage, compression, and raster size matter.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INPUT_TIF="$SCRIPT_DIR/data/input.tif"
COG_TIF="$SCRIPT_DIR/output/output_cog.tif"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

for file in "$INPUT_TIF" "$COG_TIF"; do
  if [[ ! -f "$file" ]]; then
    echo "Required raster not found: $file" >&2
    echo "Run examples/01-cog-creation/run.sh first and provide data/input.tif." >&2
    exit 2
  fi
done

echo "=== File size comparison ==="
ls -lh "$INPUT_TIF" "$COG_TIF"

echo "=== Local full-raster read (timing is indicative, not a benchmark) ==="
time gdal_translate -q -of GTiff "$INPUT_TIF" "$TMP_DIR/full-input.tif"
time gdal_translate -q -of GTiff "$COG_TIF" "$TMP_DIR/full-cog.tif"

echo "=== Windowed read using the example's EPSG:4326 bounds ==="
time gdal_translate -q -of GTiff -projwin -80.93 29.03 -80.92 29.02 "$INPUT_TIF" "$TMP_DIR/window-input.tif"
time gdal_translate -q -of GTiff -projwin -80.93 29.03 -80.92 29.02 "$COG_TIF" "$TMP_DIR/window-cog.tif"

echo "Outputs were written to a temporary directory and removed on exit."
echo "For meaningful remote range-request measurements, repeat against the same object store and control cache state."
