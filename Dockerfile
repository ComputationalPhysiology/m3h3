FROM quay.io/fenicsproject/stable

USER root

RUN apt-get -qq update && \
    apt-get -y upgrade && \
    apt-get -y install python3-scipy mercurial && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Update pip
RUN pip install --upgrade pip

# Reinstall h5py without binaries
RUN pip uninstall h5py
RUN pip install h5py --no-binary=h5py

# Install cbcbeat
RUN hg clone https://bitbucket.org/meg/cbcbeat
RUN cd cbcbeat; pip install .; cd ..

# Install pulse
RUN pip install git+https://github.com/finsberg/pulse.git

# Install fenics-geometry
RUN pip install git+https://github.com/ComputationalPhysiology/fenics-geometry.git
