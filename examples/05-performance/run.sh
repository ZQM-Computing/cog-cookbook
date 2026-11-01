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

# Return GDAL's checksum for the first band. This is a practical regression
# check for these local reads, not a cryptographic or byte-for-byte comparison.
raster_checksum() {
  gdalinfo -json -checksum "$1" |
    python3 -c 'import json, sys; print(json.load(sys.stdin)["bands"][0]["checksum"])'
}

raster_width() {
  gdalinfo -json "$1" |
    python3 -c 'import json, sys; print(json.load(sys.stdin)["size"][0])'
}

echo "=== File size comparison ==="
ls -lh "$INPUT_TIF" "$COG_TIF"

echo "=== Local full-raster read (timing is indicative, not a benchmark) ==="
time gdal_translate -q -of GTiff "$INPUT_TIF" "$TMP_DIR/full-input.tif"
time gdal_translate -q -of GTiff "$COG_TIF" "$TMP_DIR/full-cog.tif"

input_full_checksum="$(raster_checksum "$TMP_DIR/full-input.tif")"
cog_full_checksum="$(raster_checksum "$TMP_DIR/full-cog.tif")"
if [[ "$input_full_checksum" != "$cog_full_checksum" ]]; then
  echo "Full-raster read mismatch: source checksum $input_full_checksum, COG checksum $cog_full_checksum" >&2
  exit 1
fi
echo "Full-raster pixel checksums match: $input_full_checksum"

echo "=== Windowed read using the example's EPSG:4326 bounds ==="
time gdal_translate -q -of GTiff -projwin -80.93 29.03 -80.92 29.02 "$INPUT_TIF" "$TMP_DIR/window-input.tif"
time gdal_translate -q -of GTiff -projwin -80.93 29.03 -80.92 29.02 "$COG_TIF" "$TMP_DIR/window-cog.tif"

input_window_checksum="$(raster_checksum "$TMP_DIR/window-input.tif")"
cog_window_checksum="$(raster_checksum "$TMP_DIR/window-cog.tif")"
if [[ "$input_window_checksum" != "$cog_window_checksum" ]]; then
  echo "Windowed read mismatch: source checksum $input_window_checksum, COG checksum $cog_window_checksum" >&2
  exit 1
fi
window_width="$(raster_width "$TMP_DIR/window-input.tif")"
source_width="$(raster_width "$TMP_DIR/full-input.tif")"
if (( window_width >= source_width )); then
  echo "Windowed read did not reduce raster width ($window_width >= $source_width)." >&2
  exit 1
fi
echo "Windowed pixel checksums match: $input_window_checksum"
echo "Window width $window_width is smaller than full raster width $source_width."

echo "Outputs were written to a temporary directory and removed on exit."
echo "Checksums establish local pixel-value agreement for these reads; they do not measure remote range requests."
echo "For meaningful remote range-request measurements, repeat against the same object store and control cache state."
