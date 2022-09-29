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
LABEL version="1.1.5.dev0"
LABEL description="User environment for AVL JupyterHub deployment"

# We need to be root to install system-wide packages with apt.

USER root

# Install available apt package upgrades to fix known vulnerabilities in the
# base image, then install additional apt packages which might be useful in
# the user environment.

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    otb-bin=7.0.0+dfsg-2build3 \
    yarnpkg=1.22.4-2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Use the jovyan user for installs in the conda environment to avoid polluting
# it with files owned by root. The NB_UID environment variable is inherited
# from the base image which ultimately inherits it from base-notebook.

USER ${NB_UID}

# The Jupyter images have mamba preinstalled and conda-forge as the default
# channel. First we update mamba to a more recent version.

RUN mamba install mamba=0.25.0

# Package versions are explicitly pinned to ensure a well-defined, reproducible
# environment. This package list should be kept in alphabetical order to make
# it easy to find specific packages in it.

RUN mamba install --yes \
    'agriculture-vlab==0.2.0' \
    'contextily==1.2.0' \
    'dask==2022.3.0' \
    'dask-labextension==5.3.0' \
    'earthpy==0.9.4' \
    'graphviz==6.0.1' \
    'jupyterlab-geojson==3.2.0' \
    'jupyterlab-git==0.39.2' \
    'jupyterlab-github==3.0.1' \
    'nc-time-axis==1.4.1' \
    'plotly==5.10.0' \
    'pygraphviz==1.10' \
    'python-graphviz==0.20.1' \
    'rasterstats==0.17.0' \
    'rioxarray==0.12.0' \
    'sentinelhub==3.4.4' \
    'voila==0.3.6' \
    'xarray==2022.6.0' \
    'xcube==0.12.0' \
    'xcube-cci==0.9.6' \
    'xcube-cds==0.9.1' \
    'xcube_geodb==1.0.4' \
    'xcube-sh==0.9.5'

# Print a package list in case we need it for diagnostics or debugging.

RUN mamba list

# Copy the user init file to a location where it will be automatically run
# whenever a notebook is opened.

COPY init.py /home/jovyan/.ipython/profile_default/startup/init.py

# Set the default user and home directory. The environment variables are
# inherited from the base image which ultimately inherits them from
# base-notebook.

USER ${NB_UID}
WORKDIR "${HOME}"
