DMSC Instrument Data Documents
==============================

See [European Spallation Source](https://europeanspallationsource.se/).

Creating .pdfs
-------------

The simplest option is to use the helper script `make_pdf.sh`:
```
git clone git@github.com:DMSC-Instrument-Data/documents.git
cd documents
./make_pdf.sh
```
Generated `.pdf` files can be found in `pdf/` (which is actually a symlink to `build/pdf/`).

Alternatively, you can use a `cmake` out-of-source build to create `.pdf` output files:
```
git clone git@github.com:DMSC-Instrument-Data/documents.git
mkdir build
cd build
cmake ../documents/
make
```
Generated `.pdf` files can be found in the folder `pdf/`.
