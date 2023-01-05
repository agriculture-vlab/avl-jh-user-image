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
FROM quay.io/bcdev/scipy-notebook:python-3.9.13

LABEL maintainer="pontus.lurcock@brockmann-consult.de"
LABEL name="avl-user-env"
LABEL version="2.0.0-beta.3"
LABEL description="User environment for AVL JupyterHub deployment"

# We need to be root to install system-wide packages with apt.

USER root

# Install available apt package upgrades to fix known vulnerabilities in the
# base image, then install additional apt packages which might be useful in
# the user environment.

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes \
    && apt-get upgrade --yes \
    && apt-get install --yes --no-install-recommends \
    rsync \
    s3cmd \
    yarnpkg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Use the jovyan user for installs in the conda environment to avoid polluting
# it with files owned by root. The NB_UID environment variable is inherited
# from the base image which ultimately inherits it from base-notebook.

USER ${NB_UID}

# The Jupyter images have mamba preinstalled and conda-forge as the default
# channel. First we update mamba to a more recent version.

RUN mamba install mamba=1.1.0 --yes && \
    mamba clean --all -f --yes

# In contrast to the apt packages above, we don't run a general "mamba update"
# here because it would make the conda environment very hard to reproduce,
# and we don't always necessarily want the latest versions. However, the
# "mamba install" below will also upgrade various dependencies of the explicitly
# requested packages.

# This package list below should be kept in alphabetical order to make it easy
# to find specific packages in it. widgetsnbextension seems to get uninstalled
# by the mamba update for some reason so we reinstall it explicitly here.

# The py-xgboost package auto-selects the -cpu or -gpu variant on installation.

RUN mamba install --yes \
    'agriculture-vlab==0.2.0' \
    'click==8.1.3' \
    'coiled==0.2.52' \
    'contextily==1.2.0' \
    'dask==2022.11.1' \
    'dask-labextension==6.0.0' \
    'dask-ml==2022.5.27' \
    'distributed==2022.11.1' \
    'earthpy==0.9.4' \
    'fsspec==2022.11.0' \
    'gcsfs==2022.11.0' \
    'graphviz==6.0.2' \
    'ipywidgets==7.7.2' \
    'jupyterlab==3.5.2' \
    'jupyterlab-geojson==3.3.1' \
    'jupyterlab-git==0.40.1' \
    'jupyterlab-github==3.0.1' \
    'lz4==4.0.2' \
    'nb_conda_kernels==2.3.1' \
    'nc-time-axis==1.4.1' \
    'nodejs==18.12.1' \
    'numba==0.56.4' \
    'numpy==1.23.5' \
    'pandas==1.5.2' \
    'pip==22.3.1' \
    'plotly==5.11.0' \
    'py-xgboost==1.7.1' \
    'pyarrow==9.0.0' \
    'pygraphviz==1.10' \
    'python-graphviz==0.20.1' \
    'python-snappy==0.6.1' \
    'rasterstats==0.17.0' \
    'rioxarray==0.13.1' \
    's3fs==2022.11.0' \
    'scikit-learn==1.1.3' \
    'scipy==1.8.0' \
    'sentinelhub==3.4.4' \
    'widgetsnbextension==3.6.1' \
    'xarray==2022.11.0' \
    'xcube==0.12.1' \
    'xcube-cci==0.9.6' \
    'xcube-cds==0.9.1' \
    'xcube-cmems==0.1.0' \
    'xcube-sh==0.9.5' \
    'xcube_geodb==1.0.4' \
    'zarr==2.13.3' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

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
