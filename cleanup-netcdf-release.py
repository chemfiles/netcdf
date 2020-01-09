import os
import glob
import shutil
import urllib.request
import subprocess

# Update the version number here to clean a newer release.
VERSION = 'v4.7.3'
LOCALE_ARCHIVE = f'{VERSION}.tar.gz'

if not os.path.exists(LOCALE_ARCHIVE):
    print(f'downloading netcdf release {VERSION}')
    url = f'https://github.com/Unidata/netcdf-c/archive/{VERSION}.tar.gz'
    urllib.request.urlretrieve(url, LOCALE_ARCHIVE)


subprocess.run(["tar", "xf", LOCALE_ARCHIVE])
subprocess.run(["mv", f"netcdf-c-{VERSION[1:]}", "netcdf"])

KEEP_DIRECTORIES = [
    "include",
    "liblib",
    "libsrc",
    "libdispatch",
    "libdispatch",
]

# Remove extra directory, this makes the loop below easier
for f in glob.glob('netcdf/*/'):
    path = '/'.join(f.split('/')[1:-1])
    if path not in KEEP_DIRECTORIES:
        shutil.rmtree(f)

KEEP_FILES = [
    "COPYRIGHT",
    "README.md",
    "config.h.cmake.in",
    "libdispatch/utf8proc_data.c",
]

with open("CMakeLists.txt") as fd:
    in_sources = False
    for line in fd:
        if "NETCDF_SOURCES" in line:
            in_sources = True
        if in_sources and ")" in line:
            break

        if in_sources:
            if "#" in line:
                continue
            KEEP_FILES.extend(line.split())

# Remove extra files
for pattern in ['netcdf/*', 'netcdf/*/*']:
    for f in glob.glob(pattern):
        if not os.path.isfile(f):
            continue
        path = '/'.join(f.split('/')[1:])
        if path not in KEEP_FILES:
            os.unlink(f)

# remove hidden files
subprocess.run(["rm", "-rf", "netcdf/.github"])
subprocess.run(["rm", "-f", "netcdf/.travis.yml"])

with open("CMakeLists.txt") as fd:
    with open(f'netcdf/CMakeLists.txt', 'w') as output:
        output.write(f'set(VERSION {VERSION[1:]})\n')
        output.write(f'set(PACKAGE_VERSION {VERSION[1:]})\n')

        output.write(fd.read())

subprocess.run(["tar", "cf", "netcdf.tar", "netcdf"])
subprocess.run(["gzip", "-9", "netcdf.tar"])
subprocess.run(["rm", "-rf", "netcdf"])

print("done !")
