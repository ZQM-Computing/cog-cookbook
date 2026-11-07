# Cloud Optimized GeoTIFF (COG) Cookbook

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![GitHub](https://img.shields.io/github/stars/ZQM-Computing/cog-cookbook?style=social)
[![CI](https://github.com/ZQM-Computing/cog-cookbook/actions/workflows/ci.yml/badge.svg)](https://github.com/ZQM-Computing/cog-cookbook/actions/workflows/ci.yml)

A **Cloud Optimized GeoTIFF (COG) cookbook** for creating, inspecting, validating, and serving cloud-friendly raster imagery. Examples cover raster layout checks, local synthetic fixtures, optional TiTiler tile serving, and xarray-based analysis. It is intended for GIS analysts, remote-sensing practitioners, and geospatial data engineers; remote services and production object storage require separate setup and validation.

## Repository role and status

**Status:** Active, public.

**What this repository is:** Cloud Optimized GeoTIFF (COG) patterns — creating, validating, serving as tiles (including TiTiler), and lazily reading cloud-native rasters, with xarray integration.

**What it contributes:** Part of the ZQM Computing geospatial portfolio. This repository provides examples and guidance for the tools and workflows described below; validate each example against your own data, software versions, and operating environment before adopting it. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** This repository is maintained independently. Automated checks cover only the paths and environments configured in its workflows; they do not establish production readiness or operational certification.

## Who this is for

Geospatial developers, cloud engineers, and data engineers who store and serve large raster datasets from object storage. A COG is a regular GeoTIFF with internal tiling and overviews, which means HTTP range requests can fetch just the window you need.

## Prerequisites

- GDAL >= 3.6 with command-line utilities (`gdal-bin`)
- Python 3.11+ for the xarray example (`xarray`, `rioxarray`)
- Bash

```bash
# Ubuntu
sudo apt-get install gdal-bin
pip install xarray rioxarray
```

## Quickstart

```bash
cd examples/01-cog-creation
chmod +x run.sh
./run.sh
```

Examples write to an `output/` directory next to each script. Example 01 expects `examples/01-cog-creation/data/input.tif`. Create a small synthetic input with GDAL, or supply your own GeoTIFF:

```bash
mkdir -p examples/01-cog-creation/data
gdal_create -outsize 512 512 -bands 1 -burn 7 \\
  -a_srs EPSG:4326 -a_ullr -80.94 29.04 -80.91 29.01 \\
  examples/01-cog-creation/data/input.tif
bash examples/01-cog-creation/run.sh
```

## Patterns

| # | Example | What it demonstrates |
| --- | --------- | ---------------------- |
| 01 | `01-cog-creation` | Creating COGs with `gdal_translate -of COG`: DEFLATE vs. ZSTD, forced internal overviews for small inputs |
| 02 | `02-validation` | Fail-closed COG validation using GDAL JSON metadata: GeoTIFF driver, dimensions, bands, CRS, and explicit COG layout |
| 03 | `03-titiler-serving` | Serving COGs as dynamic map tiles with TiTiler |
| 04 | `04-xarray-integration` | Lazy, windowed reads of COGs with xarray + rioxarray |
| 05 | `05-performance` | Indicative local full-raster and windowed reads, with source-vs-COG pixel-checksum equivalence checks |
| 06 | `06-full-workflow` | End-to-end: create → validate → serve → analyze |
| 07 | `07-source-cog-integrity` | Fail-closed synthetic GeoTIFF → COG comparison with source/COG hashes, CRS, geotransform, pixel checksums and overview evidence |

## Did raster conversion preserve values and location?

The [source-versus-COG integrity walkthrough](docs/source-vs-cog-integrity.md) provides a **seventh executable recipe** that compares local synthetic source/COG pixel checksums, CRS/geotransform, band types, nodata metadata, sizes, SHA-256 provenance and strictly descending internal overviews. Its JSON output is evidence about a local fixture only—not a cloud range-request benchmark, bitwise proof for every raster type, or an environmental risk finding. Run it after Example 01 with Python 3.11+ and GDAL.

## Repository layout

```text
cog-cookbook/
├── examples/
│   ├── 01-cog-creation/run.sh
│   ├── 02-validation/run.sh
│   ├── 03-titiler-serving/run.sh
│   ├── 04-xarray-integration/run.py
│   ├── 05-performance/run.sh
│   ├── 06-full-workflow/run.sh
│   └── 07-source-cog-integrity/run.py
├── tests/
│   ├── test_patterns.py     # inventory, runtime GDAL smoke tests
│   └── test_cog_integrity.py # metadata failure-path tests
├── pyproject.toml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Validation

```bash
python -m pip install pytest ruff
python -m ruff check examples tests
python -m ruff format --check examples tests
python -m pytest -q
```

The suite checks the exact example inventory, shell syntax, Python syntax, and repository metadata. CI also enforces Ruff lint and formatting checks across `examples/` and `tests/`. When GDAL CLI tools are installed, it also creates a synthetic raster and executes examples 01, 02, 05, and 06, checking key output artifacts and raster metadata. Example 07 additionally compares local source/COG evidence and rejects ordinary GeoTIFF outputs or mismatched raster properties. Example 05 compares GDAL band checksums for full and windowed local reads from the source GeoTIFF and generated COG, and verifies that the requested window is narrower than the full raster; its timings remain illustrative rather than a controlled benchmark. Example 02 exits nonzero when GDAL cannot positively identify the input as a COG; it is a local metadata gate, not a substitute for independent conformance validation or remote HTTP range-request testing. CI installs `gdal-bin` and runs this integration path. The TiTiler example documents server invocation but does not launch a service in CI; the xarray example is syntax-checked only and requires its documented Python dependencies and a prepared COG for runtime use.

## Roadmap

- `rio-cogeo validate` as an alternative validation path
- COG + STAC pairing walkthrough (see [stac-cookbook](https://github.com/ZQM-Computing/stac-cookbook) example 08)
- Internal mask vs. sidecar mask trade-offs

## Contributing

See [CONTRIBUTING.md](https://github.com/ZQM-Computing/cog-cookbook/blob/main/CONTRIBUTING.md). Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [postgis-cookbook](https://github.com/ZQM-Computing/postgis-cookbook) — PostGIS SQL examples: spatial indexing, joins & KNN, SRID management, vector tiles, data quality, partitioning
- [duckdb-spatial-cookbook](https://github.com/ZQM-Computing/duckdb-spatial-cookbook) — DuckDB Spatial patterns for analytical geospatial SQL: GeoParquet, spatial joins, KNN, H3 aggregation — no server required
- [pgrouting-cookbook](https://github.com/ZQM-Computing/pgrouting-cookbook) — pgRouting network analysis on PostGIS: shortest path, driving distance, isochrones, turn restrictions, traffic-aware routing
- [geopandas-cookbook](https://github.com/ZQM-Computing/geopandas-cookbook) — GeoPandas/Shapely patterns for Python geospatial workflows: spatial joins, CRS handling, overlays, interpolation, performance
- [gdal-cookbook](https://github.com/ZQM-Computing/gdal-cookbook) — GDAL/OGR command-line examples for conversion, reprojection, clipping, and mosaicking
- [stac-cookbook](https://github.com/ZQM-Computing/stac-cookbook) — STAC patterns for geospatial data discovery: catalogs, item validation, search API, bulk operations, cloud deployment
- [maplibre-cookbook](https://github.com/ZQM-Computing/maplibre-cookbook) — MapLibre GL JS patterns for frontend vector tile rendering: custom layers, 3D terrain, performance tuning, interactive maps
- [geoparquet-cookbook](https://github.com/ZQM-Computing/geoparquet-cookbook) — GeoParquet patterns for columnar geospatial analytics: partitioning, predicate pushdown, DuckDB/Spark integration
- [h3-cookbook](https://github.com/ZQM-Computing/h3-cookbook) — H3 hexagonal grid patterns: indexing, aggregation, visualization, grid comparisons, performance benchmarks
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS snippets, Processing scripts, styles, and QField field-collection guides
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API – Features reference implementation with FastAPI and PostGIS backends
- [ollama-fleet-cookbook](https://github.com/ZQM-Computing/ollama-fleet-cookbook) — Ollama fleet operations: model management, health checks, load-spreading, VRAM budgeting, dependency-light RAG
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks: health checks, backup discipline, OSD replacement, upgrade checklists
- [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks) — Umbrella index for ZQM Computing geospatial cookbooks

## Documentation and validation

For setup instructions, reproducible examples, data provenance, CRS/SRID assumptions, security guidance, and dependency labels, follow the [ZQM geospatial repository documentation standard](https://github.com/ZQM-Computing/geospatial-cookbooks/blob/main/docs/repository-documentation-standard.md).

The configured CI workflow is the source of truth for automated checks. A passing workflow establishes only that its checks passed for that commit; it does not certify production deployment or prove that every dependency and operating environment was covered.

## License

MIT — see LICENSE file.

*Part of [ZQM Computing](https://github.com/ZQM-Computing) — geospatial engineering, scientific computing, and infrastructure patterns; the geospatial arm of [ZQM Labs](https://zqmlabs.com), makers of Z's Quests & Mischief location games.*
