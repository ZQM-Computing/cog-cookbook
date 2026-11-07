# How can I verify a Cloud Optimized GeoTIFF preserved my raster?

**Answer:** validate the generated file as a COG, then compare the
source raster's **size, CRS, geotransform, bands, nodata metadata
and per-band GDAL checksums**, and inspect the internal overview
pyramid. Record both file hashes for provenance. Passing these
checks is useful evidence for **this one fixture** but is not proof
of scientific accuracy, lossless equivalence for every type, or remote
range-read speed.

## Run a local, synthetic example

Prerequisites: Python 3.11+, GDAL 3.6 or newer, `gdal_create`,
`gdal_translate`, and `gdalinfo`.

From the repository root:

```bash
mkdir -p examples/01-cog-creation/data
gdal_create -outsize 512 512 -bands 1 -burn 7 \
  -a_srs EPSG:4326 -a_ullr -80.94 29.04 -80.91 29.01 \
  examples/01-cog-creation/data/input.tif
bash examples/01-cog-creation/run.sh
python examples/07-source-cog-integrity/run.py \
  examples/01-cog-creation/data/input.tif \
  examples/01-cog-creation/output/output_overviews.tif \
  --output /tmp/cog-integrity-evidence.json
```

This recipe creates a 512×512 synthetic single-band GeoTIFF
containing the constant value 7, converts it with GDAL's COG
driver and intentionally requests internal overviews. The
evidence command reads **local files only**. It calls GDAL
to inspect them and rejects missing or mismatched properties.

## What is in the evidence report?

The resulting machine-readable JSON contains:

| Field | What it proves and does not prove |
| --- | --- |
| Source and COG SHA-256 digests | File identity/provenance; the hashes need **not** match |
| Byte sizes | Exact local file sizes, **not** upload speed or HTTP transfer |
| Pixel dimensions and band count | Basic structural equivalence |
| CRS and geotransform checks | Matching GDAL metadata; not a field-survey accuracy claim |
| GDAL per-band checksums | Local agreement for this raster's sample values; these checksums are **not cryptographic** |
| Nodata and data type | Metadata agrees, not proof that every masked-pixel edge case is correct |
| Overview sizes | The internal pyramid is present and strictly decreasing in width and height |

Fail-closed conditions include an ordinary GeoTIFF mislabeled as a COG,
different CRS, shifted geotransform, pixel checksum mismatch, incompatible
nodata/type, missing overview and malformed dimension metadata.

## Why not conclude that the COG is faster?

A Cloud Optimized GeoTIFF allows suitably configured object-storage
servers and readers to request portions of a raster efficiently.
This local smoke test makes **no** HTTP range request, controls no
cloud cache, and establishes no read/transfer-time advantage. For
a defensible performance claim, test the identical imagery on the
same server under documented cold/warm cache conditions and
record bandwidth, byte ranges, transfer bytes, response codes,
software versions, number of runs and result equivalence.

## Production and environmental screening boundary

Use source data with documented rights, temporal coverage, resolution,
CRS, nodata semantics and uncertainty. Synthetic constant pixels do not
represent actual hazards, environmental change or regulatory findings.
A measured zero is not equivalent to absence of source coverage;
see the [DuckDB Spatial missing-coverage example](https://github.com/ZQM-Computing/duckdb-spatial-cookbook/blob/main/docs/unknown-vs-zero-parcel-screening.md).

This is a **reproducible cookbook QA example**, not a certified
survey, engineering opinion, environmental clearance, production
object-store benchmark, or independently verified customer result.
