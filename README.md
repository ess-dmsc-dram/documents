DMSC Instrument Data Documents
==============================

See [European Spallation Source](https://europeanspallationsource.se/).

Creating pdfs
-------------

Use a `cmake` out-of-source build to create `pdf` output files:
```
git clone git@github.com:DMSC-Instrument-Data/documents.git
mkdir build
cd build
cmake ../documents/
make
```
Generated `pdf` files can be found in the folder `pdf/`.
