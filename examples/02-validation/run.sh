#!/usr/bin/env bash
# Example 02: Inspect and strictly validate a Cloud Optimized GeoTIFF.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INPUT_DIR="$SCRIPT_DIR/data"
INPUT_TIF="${COG_FILE:-$INPUT_DIR/input.tif}"
OUTPUT_DIR="$SCRIPT_DIR/output"
mkdir -p "$OUTPUT_DIR"

if [[ ! -f "$INPUT_TIF" ]]; then
  echo "Input raster not found: $INPUT_TIF" >&2
  echo "Set COG_FILE=/path/to/a/COG.tif or place input.tif in $INPUT_DIR." >&2
  exit 2
fi

echo "=== Inspect and validate COG metadata ==="
python3 - "$INPUT_TIF" <<'PY'
import json
import subprocess
import sys

path = sys.argv[1]
result = subprocess.run(
    ["gdalinfo", "-json", path],
    check=True,
    capture_output=True,
    text=True,
)
info = json.loads(result.stdout)
metadata = info.get("metadata", {})
image_structure = metadata.get("IMAGE_STRUCTURE", {})
size = info.get("size", [])
bands = info.get("bands", [])
crs_present = bool(info.get("coordinateSystem", {}).get("wkt"))

print(f"File: {path}")
print(f"Driver: {info.get('driverShortName', 'unknown')}")
print(f"Size: {size}")
print(f"CRS present: {crs_present}")
print(f"Band count: {len(bands)}")
print(f"Image structure: {image_structure}")

issues = []
if info.get("driverShortName") != "GTiff":
    issues.append("dataset driver is not GTiff")
if not (isinstance(size, list) and len(size) == 2 and all(isinstance(n, int) and n > 0 for n in size)):
    issues.append("raster dimensions are missing or invalid")
if not bands:
    issues.append("raster has no bands")
if not crs_present:
    issues.append("CRS metadata is missing")
if image_structure.get("LAYOUT") != "COG":
    issues.append(
        "GDAL does not identify this file as a COG (IMAGE_STRUCTURE.LAYOUT != COG)"
    )

if issues:
    print("COG validation FAILED:", file=sys.stderr)
    for issue in issues:
        print(f"  - {issue}", file=sys.stderr)
    sys.exit(1)

print("COG validation PASSED.")
PY

echo "=== File and overview summary ==="
ls -lh "$INPUT_TIF"
gdalinfo "$INPUT_TIF" | grep -E "Overviews:|Block=" || true
