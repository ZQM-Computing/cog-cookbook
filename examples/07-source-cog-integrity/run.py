"""Compare a local synthetic source GeoTIFF with a generated COG.

Usage:
  python examples/07-source-cog-integrity/run.py \
    examples/01-cog-creation/data/input.tif \
    examples/01-cog-creation/output/output_overviews.tif \
    --output /tmp/cog-evidence.json

Requires only Python 3.11+ and the gdalinfo command-line tool.
This is a fail-closed, local metadata and pixel-checksum smoke test;
it is not proof of HTTP range behavior, bitwise raster equivalence,
or environmental truth.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path


def _info(path: Path) -> dict:
    result = subprocess.run(
        ["gdalinfo", "-json", "-checksum", str(path)],
        capture_output=True,
        text=True,
        check=True,
        timeout=45,
    )
    data = json.loads(result.stdout)
    if not isinstance(data, dict):
        raise TypeError("gdalinfo output is not a JSON object")
    return data


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _positive_size(info: dict) -> list[int]:
    size = info.get("size")
    if not isinstance(size, list) or len(size) != 2 or any(type(n) is not int or n <= 0 for n in size):
        raise ValueError("Invalid raster width/height in GDAL metadata")
    return size


def _transform(info: dict) -> list[float]:
    values = info.get("geoTransform")
    if not isinstance(values, list) or len(values) != 6:
        raise ValueError("Missing six-element geotransform")
    if any(type(n) not in (int, float) or not math.isfinite(n) for n in values):
        raise ValueError("Invalid geotransform")
    return values


def _overview_sizes(band: dict, full: list[int]) -> list[list[int]]:
    values = band.get("overviews", [])
    if not isinstance(values, list) or not values:
        raise ValueError("The COG is missing internal overviews")
    sizes = []
    width, height = full
    for item in values:
        if not isinstance(item, dict):
            raise TypeError("Malformed overview metadata")
        size = _positive_size(item)
        if size[0] >= width or size[1] >= height:
            raise ValueError("COG overview dimensions must decrease")
        sizes.append(size)
        width, height = size
    return sizes


def analyze(source: Path, cog: Path) -> dict:
    if not source.is_file() or not cog.is_file():
        raise ValueError("Both source and COG must be existing local files")
    a, b = _info(source), _info(cog)
    if a.get("driverShortName") != "GTiff" or b.get("driverShortName") != "GTiff":
        raise ValueError("Expected source and output to be GeoTIFF")
    if b.get("metadata", {}).get("IMAGE_STRUCTURE", {}).get("LAYOUT") != "COG":
        raise ValueError("GDAL does not identify the output as COG")
    size = _positive_size(a)
    if _positive_size(b) != size:
        raise ValueError("Source and COG raster dimensions differ")
    crs_a = a.get("coordinateSystem", {}).get("wkt")
    crs_b = b.get("coordinateSystem", {}).get("wkt")
    if not isinstance(crs_a, str) or not crs_a or crs_a != crs_b:
        raise ValueError("Source and COG CRS metadata differ")
    transform_a, transform_b = _transform(a), _transform(b)
    if not all(math.isclose(x, y, rel_tol=0.0, abs_tol=1e-10) for x, y in zip(transform_a, transform_b)):
        raise ValueError("Source and COG geotransforms differ")
    bands_a, bands_b = a.get("bands"), b.get("bands")
    if not isinstance(bands_a, list) or not bands_a or not isinstance(bands_b, list):
        raise ValueError("Missing GDAL band metadata")
    if len(bands_a) != len(bands_b):
        raise ValueError("Raster band counts differ")

    report_bands = []
    for number, (source_band, cog_band) in enumerate(zip(bands_a, bands_b), 1):
        if not isinstance(source_band, dict) or not isinstance(cog_band, dict):
            raise TypeError("Invalid band metadata")
        checksum_a = source_band.get("checksum")
        checksum_b = cog_band.get("checksum")
        if type(checksum_a) is not int or type(checksum_b) is not int or checksum_a != checksum_b:
            raise ValueError("GDAL pixel checksum mismatch (band " + str(number) + ")")
        if source_band.get("type") != cog_band.get("type"):
            raise ValueError("Band sample data types differ")
        if source_band.get("noDataValue") != cog_band.get("noDataValue"):
            raise ValueError("Band nodata metadata differ")
        report_bands.append(
            {
                "band": number,
                "sample_type": source_band.get("type"),
                "gdal_pixel_checksum": checksum_a,
                "nodata": cog_band.get("noDataValue"),
                "overview_sizes": _overview_sizes(cog_band, size),
            }
        )

    return {
        "schema_version": 1,
        "status": "local_synthetic_cog_integrity_smoke_only",
        "source_sha256": _sha256(source),
        "cog_sha256": _sha256(cog),
        "source_bytes": source.stat().st_size,
        "cog_bytes": cog.stat().st_size,
        "raster_size": size,
        "band_count": len(report_bands),
        "crs_metadata_equal": True,
        "geotransform_equal_within_1e-10": True,
        "bands": report_bands,
        "limitations": [
            "GDAL pixel checksums are not cryptographic proof of raster equivalence.",
            "Source and output can have different byte hashes while representing equal samples.",
            "COG layout metadata and overviews do not establish remote HTTP range support.",
            "A single synthetic fixture does not establish universal compression or read-speed gains.",
            "No environmental observations, risk decisions or regulatory clearance are made.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("cog", type=Path)
    parser.add_argument("--output", type=Path, help="Optional JSON report; do not overwrite input rasters")
    args = parser.parse_args()
    try:
        report = analyze(args.source, args.cog)
        content = json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n"
        if args.output is not None:
            output = args.output.resolve()
            if output in (args.source.resolve(), args.cog.resolve()):
                raise ValueError("Refusing to overwrite an input raster")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content, encoding="utf-8")
        print(content, end="")
    except (OSError, TypeError, ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
