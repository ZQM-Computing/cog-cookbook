# Cloud Optimized GeoTIFF (COG) Cookbook

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a> •
  <a href="https://github.com/ZQM-Labs">ZQM Labs</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

[![CI](https://github.com/ZQM-Computing/cog-cookbook/actions/workflows/ci.yml/badge.svg)](https://github.com/ZQM-Computing/cog-cookbook/actions/workflows/ci.yml)

Runnable reference examples for creating and inspecting Cloud Optimized GeoTIFFs (COGs), serving them with TiTiler, and reading them with xarray. CI executes deterministic local raster examples; remote serving and xarray integration have separate prerequisites.

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

Example 01 expects `examples/01-cog-creation/data/input.tif`. Create a small synthetic raster with `gdal_create` or provide your own GeoTIFF. Examples write outputs beside their scripts.

## Patterns

| # | Example | What it demonstrates |
| --- | --------- | ---------------------- |
| 01 | `01-cog-creation` | Creating COGs with `gdal_translate -of COG`: DEFLATE vs. ZSTD, overview levels |
| 02 | `02-validation` | Validating COG compliance — layout, overviews, IFD structure with `gdalinfo` |
| 03 | `03-titiler-serving` | Serving COGs as dynamic map tiles with TiTiler |
| 04 | `04-xarray-integration` | Lazy, windowed reads of COGs with xarray + rioxarray |
| 05 | `05-performance` | Benchmarking COG vs. raw GeoTIFF read patterns |
| 06 | `06-full-workflow` | End-to-end: create → validate → serve → analyze |

## Repository layout

```text
cog-cookbook/
├── examples/
│   ├── 01-cog-creation/run.sh
│   ├── 02-validation/run.sh
│   ├── 03-titiler-serving/run.sh
│   ├── 04-xarray-integration/run.py
│   ├── 05-performance/run.sh
│   └── 06-full-workflow/run.sh
├── tests/
│   └── test_patterns.py     # inventory, shell syntax, and GDAL runtime checks
├── pyproject.toml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Validation

```bash
pip install pytest
pytest            # checks script presence and size
```

CI installs `gdal-bin` and executes examples 01, 02, 05, and 06 against a generated synthetic raster. TiTiler serving is documented but not started in CI; the xarray example is syntax-checked and requires its optional runtime dependencies.

## Roadmap

- `rio-cogeo validate` as an alternative validation path
- COG + STAC pairing walkthrough (see [stac-cookbook](https://github.com/ZQM-Computing/stac-cookbook) example 08)
- Internal mask vs. sidecar mask trade-offs

## Contributing

See [CONTRIBUTING.md](https://github.com/ZQM-Computing/cog-cookbook/blob/main/CONTRIBUTING.md). Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [postgis-cookbook](https://github.com/ZQM-Computing/postgis-cookbook) — Production PostGIS patterns: spatial indexing, joins & KNN, SRID management, vector tiles, data quality, partitioning
- [duckdb-spatial-cookbook](https://github.com/ZQM-Computing/duckdb-spatial-cookbook) — DuckDB Spatial patterns for analytical geospatial SQL: GeoParquet, spatial joins, KNN, H3 aggregation — no server required
- [pgrouting-cookbook](https://github.com/ZQM-Computing/pgrouting-cookbook) — pgRouting network analysis on PostGIS: shortest path, driving distance, isochrones, turn restrictions, traffic-aware routing
- [geopandas-cookbook](https://github.com/ZQM-Computing/geopandas-cookbook) — GeoPandas/Shapely patterns for Python geospatial workflows: spatial joins, CRS handling, overlays, interpolation, performance
- [gdal-cookbook](https://github.com/ZQM-Computing/gdal-cookbook) — GDAL/OGR command-line patterns: conversion, reprojection, clipping, mosaicking — production-tested, runnable examples
- [stac-cookbook](https://github.com/ZQM-Computing/stac-cookbook) — STAC patterns for geospatial data discovery: catalogs, item validation, search API, bulk operations, cloud deployment
- [maplibre-cookbook](https://github.com/ZQM-Computing/maplibre-cookbook) — MapLibre GL JS patterns for frontend vector tile rendering: custom layers, 3D terrain, performance tuning, interactive maps
- [geoparquet-cookbook](https://github.com/ZQM-Computing/geoparquet-cookbook) — GeoParquet patterns for columnar geospatial analytics: partitioning, predicate pushdown, DuckDB/Spark integration
- [h3-cookbook](https://github.com/ZQM-Computing/h3-cookbook) — H3 hexagonal grid patterns: indexing, aggregation, visualization, grid comparisons, performance benchmarks
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS snippets, Processing scripts, styles, and QField field-collection guides
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API – Features reference implementation with FastAPI and PostGIS backends
- [ollama-fleet-cookbook](https://github.com/ZQM-Computing/ollama-fleet-cookbook) — Ollama fleet operations: model management, health checks, load-spreading, VRAM budgeting, dependency-light RAG
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks: health checks, backup discipline, OSD replacement, upgrade checklists
- [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks) — Umbrella index for all ZQM geospatial pattern repos

## Documentation and validation

For setup instructions, reproducible examples, data provenance, CRS/SRID assumptions, security guidance, and dependency labels, follow the [ZQM geospatial repository documentation standard](https://github.com/ZQM-Computing/geospatial-cookbooks/blob/main/docs/repository-documentation-standard.md).

The configured CI workflow is the source of truth for automated checks. A passing workflow establishes only that its checks passed for that commit; it does not certify production deployment or prove that every dependency and operating environment was covered.

## License

MIT — see LICENSE file.

## Related repositories

- [ZQM Geospatial Patterns](https://github.com/ZQM-Computing/geospatial-cookbooks) — umbrella index of all geospatial pattern repos
- [postgis-cookbook](https://github.com/ZQM-Computing/postgis-cookbook) — production PostGIS patterns & best practices
- [duckdb-spatial-cookbook](https://github.com/ZQM-Computing/duckdb-spatial-cookbook) — DuckDB Spatial patterns for analytical geospatial SQL
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API - Features with FastAPI + PostGIS
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS, styles, and QField guides
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks
- [ollama-fleet-cookbook](https://github.com/ZQM-Computing/ollama-fleet-cookbook) — Ollama fleet operations & a minimal RAG reference

*Part of [ZQM Computing](https://github.com/ZQM-Computing) — geospatial engineering, scientific computing, and infrastructure patterns; the geospatial arm of [ZQM Labs](https://zqmlabs.com), makers of Z's Quests & Mischief location games.*

<!-- ZQM-FOOTER-START -->
<!-- markdownlint-disable MD033 -->
---

<p align="center">
  <em>Play more. Plan less.</em><br>
  <a href="https://zqmlabs.com">zqmlabs.com</a> •
  <a href="https://github.com/ZQM-Labs">ZQM Labs</a> •
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-FOOTER-END -->
