# We use a standard JupyterHub image as base. The original image is hosted on
# Docker Hub, but we use our own copy on quay.io, because Docker Hub's
# anonymous pull rate limits and quay.io's lack of support for pull
# credentials cause Docker-Hub-based builds to fail on quay.io; see
# https://issues.redhat.com/browse/PROJQUAY-1299?_sscc=t for details.

# Base image source:
# https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook .
# The version is carefully selected to provide version 1.5.0 of the jupyterhub
# package, as used in the jupyterhub/k8s-hub:1.2.0 image specified in the
# default values of the z2jh 1.2.0 Helm chart. This should ensure compatibility
# with the corresponding AVL hub image and with the chart itself.
FROM quay.io/bcdev/scipy-notebook:2021-11-20

LABEL maintainer="pontus.lurcock@brockmann-consult.de"
LABEL name="avl-user-env"
LABEL version="1.1.0"
LABEL description="User environment for AVL JupyterHub deployment"

USER root

# Upgrade some packages to fix known vulnerabilities in the base image
# and/or install additional packages.

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    otb-bin=7.0.0+dfsg-2build3 \
    yarnpkg=1.22.4-2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Use the jovyan user for installs in the conda environment to avoid polluting
# it with files owned by root. The NB_UID environment variable is inherited
# from the base image.

USER ${NB_UID}

# The Jupyter images have mamba preinstalled and conda-forge as the default
# channel. First we update mamba to a more recent version.

RUN mamba install mamba=0.23.0

# Package versions are explicitly pinned to ensure a well-defined,
# reproducible environment.

RUN mamba install --yes \
    'agriculture-vlab==0.1.1' \
    'dask==2022.3.0' \
    'dask-labextension==5.2.0' \
    'graphviz==2.49.1' \
    'jupyterlab-geojson==3.1.2' \
    'jupyterlab-git==0.34.0' \
    'nc-time-axis==1.4.1' \
    'plotly==5.7.0' \
    'pygraphviz==1.9' \
    'python-graphviz==0.19.1' \
    'rasterstats==0.15.0' \
    'rioxarray==0.10.2' \
    'sentinelhub==3.3.2' \
    'voila==0.3.5' \
    'xarray==2022.3.0' \
    'xcube==0.10.2' \
    'xcube-cci==0.9.5' \
    'xcube-cds==0.9.1' \
    'xcube_geodb==1.0.2' \
    'xcube-sh==0.9.4'

RUN mamba list

# Install newer xcube and geoDB versions from their repositories.

RUN pip3 install git+https://github.com/dcs4cop/xcube@6e37dec5ab36
RUN pip3 install git+https://github.com/dcs4cop/xcube-geodb@03803a7e39d9

USER ${NB_UID}
WORKDIR "${HOME}"
