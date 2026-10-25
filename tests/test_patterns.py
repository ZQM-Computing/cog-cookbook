"""Structural and runtime tests for the COG cookbook examples."""

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

    run("01-cog-creation")
    assert (work_examples / "01-cog-creation/output/output_cog.tif").is_file()
    run("02-validation")
    run("05-performance")
    run("06-full-workflow")
    assert (work_examples / "06-full-workflow/output/output_cog.tif").is_file()
