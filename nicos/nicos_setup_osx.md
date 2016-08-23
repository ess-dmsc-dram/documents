##Instructions for installing Nicos up to run on OSX

1. checkout nicos and enter the `nicos-core` directory
```bash
git clone git://trac.frm2.tum.de/home/repos/git/frm2/nicos/nicos-core.git
```
1. Install the virtual environment package 
```bash
pip install virtualenv
```
1. Create and activate virtual environment.
```bash
virtualenv venv --no-site-packages
source venv/bin/activate
```
1. Upgrade pip
```bash
pip install --upgrade pip
pip install --upgrade wheel
```
1. Brew install the following
```bash
brew install qt --with-qt3support --build-bottle
brew install sip --build-from-source
brew install pyqt --build-from-source
brew install numpy
brew install libtiff
```
1. Create a *.pth file in `venv/lib/python2.7/site-packages/homebrew.pth` with the following contents based on the brew installed python packages above.
```bash
/usr/local/Cellar/sip/4.16.5/lib/python2.7/site-packages/
/usr/local/Cellar/pyqt/4.11.3/lib/python2.7/site-packages/
/usr/local/Cellar/numpy/1.9.2_1/lib/python2.7/site-packages/
```
1. Install [XQuartz](https://www.xquartz.org/)
1. Create simlink of the form /usr/local/include/X11 -> /opt/X11/include/X11/
```
sudo ln -s /opt/X11/include/X11/ /usr/local/include/X11
```
1. Extend the library path
```
export LIBRARY_PATH=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.10.sdk/usr/lib/:/opt/X11/lib/
```
1. Extend the include path
```bash
export C_INCLUDE_PATH=/opt/X11/include/:/usr/include/:/usr/local/include/
```
1. In `requirements.txt` (comes with nicos) replace the lines refering to `mysql-connector-python` with:
```bash
mysql-connector-python-rf
```
1. In `requirements.txt` comment out the line `nicoslivewidget`. This currently fails to compile of osx owning to a link path.
1. 
```bash
pip install -r requirements.txt 
```
1. Install pyqwt5
```bash
wget "http://downloads.sourceforge.net/project/pyqwt/pyqwt5/PyQwt-5.2.0/PyQwt-5.2.0.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fpyqwt%2F%3Fsource%3Ddlp&ts=1371067906&use_mirror=iweb"
mv "PyQwt-5.2.0.tar.gz?r=http:%2F%2Fsourceforge.net%2Fprojects%2Fpyqwt%2F?source=dlp&ts=1371067906&use_mirror=iweb" PyQwt-5.2.0.tar.gz
tar xvzf PyQwt-5.2.0.tar.gz
cd PyQwt-5.2.0/configure
python configure.py -Q ../qwt-5.2 --module-install-path=../../project/venv/lib/python2.7/site-packages/PyQt4 --extra-lflags="-headerpad_max_install_names -bundle -undefined dynamic_lookup" --sip-include-dirs=../../project/venv/include/python2.7
make -j4
make install
cd ../../
```
1. Install imaging library 
```bash
pip install Pillow
```
1. Test nicos-startup
```bash
./bin/nicos-demo
```
1. Install [gr](http://gr-framework.org/)
```bash
git clone https://github.com/jheinen/gr
cd gr
python setup.py build_ext [--static-extras] install
```
