"""Structural and runtime tests for the COG cookbook examples."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"
EXPECTED_EXAMPLES = {
    "01-cog-creation",
    "02-validation",
    "03-titiler-serving",
    "04-xarray-integration",
    "05-performance",
    "06-full-workflow",
}


def test_exact_example_inventory():
    """The README's six advertised examples exist and have entry points."""
    assert {p.name for p in EXAMPLES_DIR.iterdir() if p.is_dir()} == EXPECTED_EXAMPLES
    for name in sorted(EXPECTED_EXAMPLES):
        entry_points = list((EXAMPLES_DIR / name).glob("run.*"))
        assert len(entry_points) == 1, f"{name} must have exactly one run.* entry point"
        assert entry_points[0].stat().st_size > 0, f"{entry_points[0]} is empty"


def test_shell_examples_have_valid_syntax():
    """Every shell example passes bash's parser."""
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("bash is unavailable")
    for script in sorted(EXAMPLES_DIR.glob("*/run.sh")):
        subprocess.run([bash, "-n", str(script)], check=True, capture_output=True, text=True)


def test_python_example_has_valid_syntax():
    """Compile Python in memory without writing __pycache__ artifacts."""
    source = (EXAMPLES_DIR / "04-xarray-integration" / "run.py").read_text(encoding="utf-8")
    compile(source, "examples/04-xarray-integration/run.py", "exec")


def test_readme_and_license_exist():
    assert (ROOT / "README.md").is_file()
    assert (ROOT / "LICENSE").is_file()


@pytest.mark.integration
def test_core_raster_examples_execute_with_synthetic_input(tmp_path):
    """Run deterministic GDAL examples against a generated local raster."""
    required = ["gdal_create", "gdalinfo", "gdal_translate"]
    missing = [name for name in required if not shutil.which(name)]
    if missing:
        pytest.skip(f"GDAL CLI tools unavailable: {', '.join(missing)}")

    work_examples = tmp_path / "examples"
    shutil.copytree(EXAMPLES_DIR, work_examples)
    source = tmp_path / "synthetic-input.tif"
    subprocess.run(
        [
            "gdal_create",
            "-q",
            "-of",
            "GTiff",
            "-outsize",
            "512",
            "512",
            "-bands",
            "1",
            "-burn",
            "7",
            "-a_srs",
            "EPSG:4326",
            "-a_ullr",
            "-80.94",
            "29.04",
            "-80.91",
            "29.01",
            str(source),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    def seed(example: str, filename: str = "input.tif") -> Path:
        target = work_examples / example / "data" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        return target

    seed("01-cog-creation")
    seed("02-validation")
    seed("05-performance")
    seed("06-full-workflow")

    def run(example: str):
        subprocess.run(
            ["bash", str(work_examples / example / "run.sh")],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )

    def raster_info(path: Path) -> dict:
        result = subprocess.run(
            ["gdalinfo", "-json", str(path)],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        import json

        return json.loads(result.stdout)

    def assert_valid_raster(path: Path) -> dict:
        assert path.is_file() and path.stat().st_size > 0, f"Missing or empty raster: {path}"
        info = raster_info(path)
        assert info.get("size") == [512, 512], f"Unexpected raster dimensions: {path}"
        assert len(info.get("bands", [])) == 1, f"Unexpected band count: {path}"
        assert info.get("coordinateSystem", {}).get("wkt"), f"Missing CRS: {path}"
        return info

    def assert_cog_layout(path: Path) -> None:
        """Reject a readable GeoTIFF that does not report the COG layout."""
        info = raster_info(path)
        image_structure = info.get("metadata", {}).get("IMAGE_STRUCTURE", {})
        assert image_structure.get("LAYOUT") == "COG", (
            f"Expected GDAL to identify {path} as a Cloud Optimized GeoTIFF; "
            f"IMAGE_STRUCTURE metadata: {image_structure}"
        )

    run("01-cog-creation")
    creation_dir = work_examples / "01-cog-creation/output"
    first_cog = creation_dir / "output_cog.tif"
    assert_valid_raster(first_cog)
    for filename in ("output_cog.tif", "output_zstd.tif", "output_overviews.tif"):
        assert_cog_layout(creation_dir / filename)

    def image_structure(path: Path) -> dict:
        return raster_info(path).get("metadata", {}).get("IMAGE_STRUCTURE", {})

    assert image_structure(creation_dir / "output_cog.tif").get("COMPRESSION") == "DEFLATE"
    assert image_structure(creation_dir / "output_zstd.tif").get("COMPRESSION") == "ZSTD"
    overview_path = creation_dir / "output_overviews.tif"
    overview_info = raster_info(overview_path)
    assert_cog_layout(overview_path)
    assert image_structure(overview_path).get("COMPRESSION") == "DEFLATE"
    overview_sizes = overview_info.get("bands", [{}])[0].get("overviews", [])
    assert len(overview_sizes) >= 2, f"Expected a useful internal overview pyramid, found {overview_sizes}"
    previous_size = 512
    for overview in overview_sizes:
        size = overview.get("size")
        assert (
            isinstance(size, list)
            and len(size) == 2
            and all(isinstance(dimension, int) and dimension > 0 for dimension in size)
        ), f"Invalid overview dimensions: {overview}"
        assert size[0] < previous_size and size[1] < previous_size, (
            f"Overview dimensions must descend from the full-resolution raster: {overview_sizes}"
        )
        assert size[0] == size[1], f"Expected square overviews for the square synthetic raster: {size}"
        previous_size = size[0]
    assert overview_sizes[-1]["size"][0] <= 128, (
        f"Expected the pyramid to reach a small overview level for 512x512 input: {overview_sizes}"
    )
    # The validation example must receive the generated COG, not the source GeoTIFF.\n    shutil.copy2(first_cog, work_examples / "02-validation/data/input.tif")\n    run("02-validation")
    invalid_env = os.environ.copy()
    invalid_env["COG_FILE"] = str(source)
    rejected = subprocess.run(
        ["bash", str(work_examples / "02-validation/run.sh")],
        check=False,
        cwd=tmp_path,
        env=invalid_env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert rejected.returncode != 0, "The validator must reject a plain source GeoTIFF."
    assert "COG validation FAILED" in rejected.stderr
    performance_cog = work_examples / "05-performance/output/output_cog.tif"
    performance_cog.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(first_cog, performance_cog)
    run("05-performance")
    run("06-full-workflow")
    final_cog = work_examples / "06-full-workflow/output/output_cog.tif"
    assert_valid_raster(final_cog)
    assert_cog_layout(final_cog)
    vrt = work_examples / "06-full-workflow/output/output_cog.vrt"
    assert vrt.is_file() and vrt.stat().st_size > 0
    assert_valid_raster(vrt)
