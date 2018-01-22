#!/bin/bash
set -e

base_path=$(pwd)
prefix_path=${base_path}/dependencies/usr



# -------------------------------------------------------------
# -------------------------------------------------------------
# Install dependencies
# -------------------------------------------------------------
# -------------------------------------------------------------
cd dependencies

# -------------------------------------------------------
# Download the rpms for RHEL 7, but avoid the Mantid ones
# -------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
wget -e robots=off --accept-regex "rhel/7/x86_64/.*\.rpm" --reject-regex "mantid|poco" -A rpm -r -l 5 -nd "http://yum.isis.rl.ac.uk/rhel/7/x86_64/"

declare -a rpms=("http://mirror.centos.org/centos/7/os/x86_64/Packages/openssl-devel-1.0.2k-8.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/m/muParser-devel-2.2.3-4.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/o/OCE-devel-0.17.1-1.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-devel-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-data-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-debug-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-doc-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-foundation-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-json-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-net-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-netssl-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-odbc-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-pagecompiler-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-sqlite-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-util-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-xml-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-zip-1.6.1-2.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/poco-crypto-1.6.1-2.el7.x86_64.rpm"
"http://mirror.centos.org/centos/7/os/x86_64/Packages/krb5-devel-1.15.1-8.el7.x86_64.rpm"
"http://mirror.centos.org/centos/7/os/x86_64/Packages/libcom_err-devel-1.42.9-10.el7.x86_64.rpm"
"http://springdale.math.ias.edu/data/puias/computational/7/x86_64//muParser-2.2.3-9.sdl7.x86_64.rpm"
"http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/o/OCE-foundation-0.17.1-1.el7.x86_64.rpm"
"http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/o/OCE-modeling-0.17.1-1.el7.x86_64.rpm"
"http://mirror.centos.org/centos/7/os/x86_64/Packages/openssl-libs-1.0.2k-8.el7.x86_64.rpm"
"http://mirror.centos.org/centos/7/os/x86_64/Packages/mesa-libGLU-devel-9.0.0-4.el7.x86_64.rpm"
"http://mirror.centos.org/centos/7/os/x86_64/Packages/gperftools-devel-2.4-8.el7.x86_64.rpm"
"http://mirror.centos.org/centos/7/os/x86_64/Packages/gperftools-libs-2.4-8.el7.x86_64.rpm"
"http://mirror.centos.org/centos/7/os/x86_64/Packages/mesa-libGLU-9.0.0-4.el7.x86_64.rpm"
"http://mirror.centos.org/centos/7/os/x86_64/Packages/libunwind-1.2-2.el7.x86_64.rpm"
"http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-ipython-console-3.2.1-1.el7.noarch.rpm"
"http://mirror.centos.org/centos/7/os/x86_64/Packages/pexpect-2.3-11.el7.noarch.rpm"
"http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-path-5.2-1.el7.noarch.rpm"
"http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-simplegeneric-0.8-7.el7.noarch.rpm"
"http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/h/h5py-2.3.1-1.el7.x86_64.rpm"
"http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/liblzf-3.6-7.el7.x86_64.rpm"
"http://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/librdkafka-0.11.1-1.el7.x86_64.rpm"
"https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/librdkafka-devel-0.11.1-1.el7.x86_64.rpm"
"http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/lz4-1.7.3-1.el7.x86_64.rpm"
"ftp://mirror.switch.ch/pool/4/mirror/centos/7.4.1708/cloud/x86_64/openstack-newton/common/python2-cycler-0.10.0-2.el7.noarch.rpm"
)

download_rpm() {
wget -e robots=off -A rpm -r -l 5 -nd $1
}


for i in "${rpms[@]}"
do
echo $i
download_rpm $i
done


#Unpack all rpms
for entry in ./*.rpm
do
echo "Starting to extract ${entry}"
rpm2cpio $entry | cpio -imdv
echo "Finished extracting  ${entry}"
done


# ------------------------------------------------------------------------------
# We need to fix jsoncpp links. No idea why they are wrong, but they need fixing
# -----------------------------------------------------------------------------
cd ./usr/lib64
rm libjsoncpp.so.0
rm libjsoncpp.so
ln -s libjsoncpp.so.0.0.0 libjsoncpp.so.0
ln -s libjsoncpp.so.0.0.0 libjsoncpp.so
cd ../..

# -----------------------------------------------------------------------------
# Generate CMake
# -----------------------------------------------------------------------------
git clone https://github.com/Kitware/CMake.git
cd CMake
git checkout release
./bootstrap
gmake
cd ..

# ------------------------------------------------------------------------------
# Generate Boost with MPi
# -----------------------------------------------------------------------------
wget http://sourceforge.net/projects/boost/files/boost/1.65.0/boost_1_65_0.tar.gz
tar -xvzf boost_1_65_0.tar.gz

cd boost_1_65_0
./bootstrap.sh --prefix=${prefix_path} --with-libraries=date_time,regex,python,serialization,filesystem,mpi
echo "using mpi : : <find-shared-library>mpiCC <find-shared-library>mpi <find-shared-library>mpi_cpu <find-shared-library>mpio <find-shared-library>mpi_mtcpu <find-shared-library>mpirm <find-shared-library>mpirun <find-shared-library>mpitv ;" >> ./project-config.jam

number_of_processors=$(nproc)
export LIBRARY_PATH=$LIBRARY_PATH:/opt/ibm/platform_mpi/lib/linux_amd64
./b2 link=static,shared cxxflags=-fPIC include=/opt/ibm/platform_mpi/include/ -j ${number_of_processors} install
cd ..


# I don't know why, but the mpi.so file is not placed into usr/lib/python2.7/site-packages/boost as it should.
# We need to create it ourselves
cd ./usr/lib
mkdir -p python2.7/site-packages/boost
cp mpi.so python2.7/site-packages/boost/.
touch python2.7/site-packages/boost/__init__.py
