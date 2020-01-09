# NetCDF release cleaner for use in Chemfiles

This repository contains a script that takes a [netcdf-c
release](https://github.com/Unidata/netcdf-c/releases), and remove all the files
not used by chemfiles. This dramatically cuts down on the archive size, from
18Mib to ~500Kib.

The script also replaces the CMakeLists.txt, to adapt to chemfiles' build
system.

Running the script (with Python >= 3.7) as `python cleanup-netcdf-release.py`
will produce the `netcdf.tar.gz` archive you want.
