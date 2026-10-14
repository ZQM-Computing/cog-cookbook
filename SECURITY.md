# Security policy

## Supported version

Security fixes are applied to the `main` branch. This repository contains Cloud Optimized GeoTIFF patterns and a local TiTiler demo; it is not a hosted service.

## Reporting a vulnerability

Email **zqmcomputing@gmail.com** with the subject `cog-patterns security` if you find a vulnerability in the example code or workflow configuration. Please do not open a public issue for a sensitive report.

Include the affected file, the impact you observed, and reproduction steps when available.

## Demo note

The TiTiler demo serves local files with demo defaults. Do not point a deployment built from these examples at a bucket or directory you wouldn't want the world to read — tile servers happily serve whatever they're given.
