"""Synthetic, dependency-free quality tests for local COG evidence reporting."""

import importlib.util
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "examples" / "07-source-cog-integrity" / "run.py"
SPEC = importlib.util.spec_from_file_location("cog_evidence", FILE)
evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence)


def metadata(*, cog):
    return {
        "driverShortName": "GTiff",
        "size": [512, 512],
        "geoTransform": [-80.94, 0.00005, 0.0, 29.04, 0.0, -0.00005],
        "coordinateSystem": {"wkt": 'GEOGCRS["WGS 84"]'},
        "metadata": {"IMAGE_STRUCTURE": {"LAYOUT": "COG"}} if cog else {},
        "bands": [
            {
                "type": "Byte",
                "checksum": 278,
                "noDataValue": 0,
                "overviews": [{"size": [256, 256]}, {"size": [128, 128]}] if cog else [],
            }
        ],
    }


def inputs(tmp_path):
    source = tmp_path / "source.tif"
    output = tmp_path / "output.tif"
    source.write_bytes(b"synthetic source raster fixture")
    output.write_bytes(b"synthetic converted raster fixture")
    return source, output


def test_valid_metadata_produces_source_provenance_and_no_remote_claim(tmp_path):
    source, output = inputs(tmp_path)
    with patch.object(evidence, "_info", side_effect=[metadata(cog=False), metadata(cog=True)]):
        report = evidence.analyze(source, output)
    assert report["schema_version"] == 1
    assert report["status"] == "local_synthetic_cog_integrity_smoke_only"
    assert report["source_sha256"] != report["cog_sha256"]
    assert len(report["source_sha256"]) == 64
    assert report["band_count"] == 1
    assert report["bands"][0]["overview_sizes"] == [[256, 256], [128, 128]]
    assert report["bands"][0]["gdal_pixel_checksum"] == 278
    assert "HTTP range" in " ".join(report["limitations"])


@pytest.mark.parametrize(
    ("modification", "expected"),
    [
        (lambda info: info["metadata"]["IMAGE_STRUCTURE"].pop("LAYOUT"), "does not identify"),
        (lambda info: info.update(size=[511, 512]), "dimensions differ"),
        (lambda info: info["coordinateSystem"].update(wkt="OTHER"), "CRS metadata differ"),
        (lambda info: info["geoTransform"].__setitem__(0, -79.0), "geotransforms differ"),
        (lambda info: info["bands"][0].update(checksum=15), "checksum mismatch"),
        (lambda info: info["bands"][0].update(type="UInt16"), "sample data types differ"),
        (lambda info: info["bands"][0].update(noDataValue=2), "nodata metadata differ"),
        (lambda info: info["bands"][0].update(overviews=[]), "missing internal overviews"),
        (
            lambda info: info["bands"][0].update(overviews=[{"size": [512, 512]}]),
            "dimensions must decrease",
        ),
    ],
)
def test_invalid_generated_cog_metadata_is_rejected(tmp_path, modification, expected):
    source, output = inputs(tmp_path)
    src, dest = metadata(cog=False), metadata(cog=True)
    modification(dest)
    with patch.object(evidence, "_info", side_effect=[src, dest]), pytest.raises(ValueError, match=expected):
        evidence.analyze(source, output)


def test_nonexistent_inputs_fail_closed(tmp_path):
    missing = tmp_path / "missing.tif"
    with pytest.raises(ValueError, match="existing local files"):
        evidence.analyze(missing, missing)


def test_bad_dimensions_and_nonfinite_georeferencing_rejected():
    with pytest.raises(ValueError, match="Invalid raster"):
        evidence._positive_size({"size": [0, 100]})
    with pytest.raises(ValueError, match="Invalid geotransform"):
        evidence._transform({"geoTransform": [0, 1, float("inf"), 0, 0, -1]})
