FROM quay.io/fenicsproject/stable

USER root

RUN apt-get -qq update && \
    apt-get -y upgrade && \
    apt-get -y install python3-scipy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Update pip
RUN pip install --upgrade pip

# Install required cardiac modelling packages
RUN pip install git+https://github.com/ComputationalPhysiology/fenics-geometry.git
RUN pip install fenics-pulse
