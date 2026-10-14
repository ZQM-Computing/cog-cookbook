"""Example 04: Read COG with xarray."""
import rioxarray  # noqa: F401 - registers the rio accessor
import xarray as xr

# Open COG with xarray (via rioxarray)
ds = xr.open_dataset("output/output_cog.tif", engine="rasterio")
print("Dataset:")
print(ds)
print()

# Access data
print(f"CRS: {ds.rio.crs}")
print(f"Bounds: {ds.rio.bounds()}")
print(f"Shape: {ds.sizes}")
print()

# Read a subset (windowed read)
subset = ds.rio.slice_xy(-80.93, 29.02, -80.92, 29.03)
print(f"Subset shape: {subset.sizes}")
print(f"Subset mean: {subset.band_1.mean().values:.2f}")
