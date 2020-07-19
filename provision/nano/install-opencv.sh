#sudo apt-get install -y python3-pip libhdf5-serial-dev hdf5-tools

git clone https://github.com/JetsonHacksNano/buildOpenCV
cd buildOpenCV
./buildOpenCV.sh |& tee openCV_build.log
sudo ldconfig -v
