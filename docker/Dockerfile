# We use a standard JupyterHub image as base. The original image is hosted on
# Docker Hub, but we use our own copy on quay.io, because Docker Hub's
# anonymous pull rate limits and quay.io's lack of support for pull
# credentials cause Docker-Hub-based builds to fail on quay.io; see
# https://issues.redhat.com/browse/PROJQUAY-1299?_sscc=t for details.

# Source: https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook
FROM quay.io/bcdev/scipy-notebook:2021-09-27

LABEL maintainer="pontus.lurcock@brockmann-consult.de"
LABEL name="avl-user-env"
LABEL version="1.0.6"
LABEL description="User environment for AVL JupyterHub deployment"

USER root

# Upgrade some packages to fix known vulnerabilities in the base image,
# and install additional packages.

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    ghostscript=9.50~dfsg-5ubuntu4.5 \
    libcaca0=0.99.beta19-2.1ubuntu1.20.04.2 \
    libgcrypt20=1.8.5-5ubuntu1.1 \
    libicu66=66.1-2ubuntu2.1 \
    libnss3=2:3.49.1-1ubuntu1.6 \
    otb-bin=7.0.0+dfsg-2build3 \
    python3.8=3.8.10-0ubuntu1~20.04.2 \
    systemd=245.4-4ubuntu3.15 \
    vim-tiny=2:8.1.2269-1ubuntu5.7 \
    yarnpkg=1.22.4-2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# The Jupyter images have mamba preinstalled and conda-forge as the default
# channel. First we update mamba to a more recent version.

RUN mamba install mamba=0.22.1

# Package versions are explicitly pinned to ensure a well-defined,
# reproducible environment.

RUN mamba install --yes \
    'avl==0.1.0' \
    'dask==2022.3.0' \
    'dask-labextension==5.2.0' \
    'graphviz==2.49.1' \
    'jupyterlab-geojson==3.1.2' \
    'jupyterlab-git==0.34.0' \
    'pygraphviz==1.9' \
    'python-graphviz==0.19.1' \
    'rasterstats==0.15.0' \
    'rioxarray==0.10.2' \
    'sentinelhub==3.3.2' \
    'xarray==2022.3.0' \
    'xcube==0.10.2' \
    'xcube-cci==0.9.5' \
    'xcube-cds==0.9.1' \
    'xcube_geodb==1.0.2' \
    'xcube-sh==0.9.4'

RUN mamba list

USER ${NB_UID}
WORKDIR "${HOME}"
