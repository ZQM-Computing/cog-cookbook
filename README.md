# Cloud Optimized GeoTIFF (COG) Patterns

Production-tested COG patterns for cloud-native raster access, serving, and analysis.

## Who this is for

Geospatial developers, cloud engineers, and data engineers who serve and analyze
large raster datasets in cloud environments.

## What's inside

- `examples/` — Runnable scripts with sample data
- `tests/` — Validation tests for each pattern

## Patterns

| # | Pattern | Description |
|---|---------|-------------|
| 1 | COG creation | Convert rasters to Cloud Optimized GeoTIFF with gdal_translate |
| 2 | Validation | Verify COG compliance (layout, overviews, IFD) with gdalinfo |
| 3 | TiTiler serving | Serve COGs as dynamic tiles via TiTiler |
| 4 | Xarray integration | Open COGs lazily with xarray + rioxarray |
| 5 | Performance | Benchmark COG vs raw GeoTIFF read patterns |
| 6 | Full workflow | End-to-end: create, validate, serve, analyze |

## Requirements

- GDAL >= 3.6
- Python 3.11+
- Shell (bash)
- GDAL Python bindings (`pip install GDAL`)

## Quick start

```bash
# Install GDAL (Ubuntu)
sudo apt-get install gdal-bin python3-gdal

# Install Python deps
pip install xarray rioxarray titiler rasterio

# Run an example
cd examples/01-cog-creation
python create_cog.py
```

## License

MIT — see LICENSE file.
