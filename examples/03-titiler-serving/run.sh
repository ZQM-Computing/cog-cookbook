#!/bin/bash
# Example 03: Serve COG with TiTiler
set -e

OUTPUT_DIR="$(dirname "$0")/output"

echo "=== Start TiTiler server ==="
echo "TiTiler serves COGs as OGC API - Tiles and WMS"
echo ""
echo "Run with Docker:"
echo "  docker run -p 8080:8080 -v $(pwd)/$OUTPUT_DIR:/data developmentseed/titiler:latest"
echo ""
echo "Then access:"
echo "  http://localhost:8080/health"
echo "  http://localhost:8080/cog/info?url=/data/output_cog.tif"
echo "  http://localhost:8080/cog/tiles/{z}/{x}/{y}?url=/data/output_cog.tif"
echo ""
echo "=== Alternative: TiTiler with pgstac ==="
echo "  docker run -p 8080:8080 -v $(pwd)/$OUTPUT_DIR:/data developmentseed/titiler-pgstac:latest"
