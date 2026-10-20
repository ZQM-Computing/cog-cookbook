# Cloud Optimized GeoTIFF (COG) Patterns

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

[![CI](https://github.com/ZQM-Computing/cog-patterns/actions/workflows/ci.yml/badge.svg)](https://github.com/ZQM-Computing/cog-patterns/actions/workflows/ci.yml)

Production-tested Cloud Optimized GeoTIFF patterns for cloud-native raster access, serving, and analysis — create them, validate them, serve them as tiles, and read them lazily.

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

The scripts write to an `output/` directory next to each `run.sh`. Example 01 expects a source raster — point it at your own GeoTIFF (or drop one in as `data/input.tif`); it demonstrates DEFLATE vs. ZSTD compression and overview levels via `gdal_translate -of COG`.

## Patterns

| # | Example | What it demonstrates |
|---|---------|----------------------|
| 01 | `01-cog-creation` | Creating COGs with `gdal_translate -of COG`: DEFLATE vs. ZSTD, overview levels |
| 02 | `02-validation` | Validating COG compliance — layout, overviews, IFD structure with `gdalinfo` |
| 03 | `03-titiler-serving` | Serving COGs as dynamic map tiles with TiTiler |
| 04 | `04-xarray-integration` | Lazy, windowed reads of COGs with xarray + rioxarray |
| 05 | `05-performance` | Benchmarking COG vs. raw GeoTIFF read patterns |
| 06 | `06-full-workflow` | End-to-end: create → validate → serve → analyze |

## Repository layout

```text
cog-patterns/
├── examples/
│   ├── 01-cog-creation/run.sh
│   ├── 02-validation/run.sh
│   ├── 03-titiler-serving/run.sh
│   ├── 04-xarray-integration/run.py
│   ├── 05-performance/run.sh
│   └── 06-full-workflow/run.sh
├── tests/
│   └── test_patterns.py     # every script exists and is non-empty
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

CI runs `ruff check` / `ruff format --check` and the pytest suite on every push and pull request.

## Roadmap

- `rio-cogeo validate` as an alternative validation path
- COG + STAC pairing walkthrough (see [stac-patterns](https://github.com/ZQM-Computing/stac-patterns) example 08)
- Internal mask vs. sidecar mask trade-offs

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [postgis-patterns](https://github.com/ZQM-Computing/postgis-patterns) — Production PostGIS patterns: spatial indexing, joins & KNN, SRID management, vector tiles, data quality, partitioning
- [duckdb-spatial-patterns](https://github.com/ZQM-Computing/duckdb-spatial-patterns) — DuckDB Spatial patterns for analytical geospatial SQL: GeoParquet, spatial joins, KNN, H3 aggregation — no server required
- [pgrouting-patterns](https://github.com/ZQM-Computing/pgrouting-patterns) — pgRouting network analysis on PostGIS: shortest path, driving distance, isochrones, turn restrictions, traffic-aware routing
- [geopandas-patterns](https://github.com/ZQM-Computing/geopandas-patterns) — GeoPandas/Shapely patterns for Python geospatial workflows: spatial joins, CRS handling, overlays, interpolation, performance
- [gdal-patterns](https://github.com/ZQM-Computing/gdal-patterns) — GDAL/OGR command-line patterns: conversion, reprojection, clipping, mosaicking — production-tested, runnable examples
- [stac-patterns](https://github.com/ZQM-Computing/stac-patterns) — STAC patterns for geospatial data discovery: catalogs, item validation, search API, bulk operations, cloud deployment
- [maplibre-patterns](https://github.com/ZQM-Computing/maplibre-patterns) — MapLibre GL JS patterns for frontend vector tile rendering: custom layers, 3D terrain, performance tuning, interactive maps
- [geoparquet-patterns](https://github.com/ZQM-Computing/geoparquet-patterns) — GeoParquet patterns for columnar geospatial analytics: partitioning, predicate pushdown, DuckDB/Spark integration
- [h3-patterns](https://github.com/ZQM-Computing/h3-patterns) — H3 hexagonal grid patterns: indexing, aggregation, visualization, grid comparisons, performance benchmarks
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS snippets, Processing scripts, styles, and QField field-collection guides
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API – Features reference implementation with FastAPI and PostGIS backends
- [ollama-fleet-patterns](https://github.com/ZQM-Computing/ollama-fleet-patterns) — Ollama fleet operations: model management, health checks, load-spreading, VRAM budgeting, dependency-light RAG
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks: health checks, backup discipline, OSD replacement, upgrade checklists
- [geospatial-patterns](https://github.com/ZQM-Computing/geospatial-patterns) — Umbrella index for all ZQM geospatial pattern repos

## Documentation and validation

For setup instructions, reproducible examples, data provenance, CRS/SRID assumptions, security guidance, and dependency labels, follow the [ZQM geospatial repository documentation standard](https://github.com/ZQM-Computing/geospatial-patterns/blob/main/docs/repository-documentation-standard.md).

The configured CI workflow is the source of truth for automated checks. A passing workflow establishes only that its checks passed for that commit; it does not certify production deployment or prove that every dependency and operating environment was covered.

## License

MIT — see LICENSE file.

*Part of [ZQM Computing](https://github.com/ZQM-Computing) — geospatial engineering, scientific computing, and infrastructure patterns.*

