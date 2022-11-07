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
LABEL version="ltc22.1"
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

RUN mamba install mamba=0.27.0

# Remove the Python 3.9 version pin. Commented out for now: we should avoid
# doing this if possible.

# RUN cat /opt/conda/conda-meta/pinned && \
#     rm /opt/conda/conda-meta/pinned

# Package versions are explicitly pinned to ensure a well-defined, reproducible
# environment (at least regarding the packages specified here). This package
# list should be kept in alphabetical order to make it easy to find specific
# packages in it. widgetsnbextension seems to get uninstalled by the mamba
# update for some reason so we reinstall it explicitly here.

# TODO: re-add voila package to install list. voila was removed on 2022-09-30
# because (as of version 0.3.6) it's incompatible with ipywidgets 8. Future
# voila versions (from 0.4.0) are planned to be compatible with ipywidgets 8.

# The py-xgboost package auto-selects the -cpu or -gpu variant on installation.


RUN mamba install --yes --channel conda-forge --channel main \
    'adjusttext>=0.7.3.1' \
    'agriculture-vlab==0.2.0' \
    'async_generator>=1.10' \
    'basemap>=1.2.1' \
    'bokeh' \
    'cartopy' \
    'cftime>=1.5.0' \
    'cmasher>=1.6.2' \
    'cmcrameri>=1.3' \
    'colorama>=0.4.4' \
    'colorspacious>=1.1.2' \
    'contextily==1.2.0' \
    'cython' \
    'dask-labextension==5.3.0' \
    'dask-ml==2022.5.27' \
    'dask==2022.6.1' \
    'e13tools>=0.9.6' \
    'earthpy==0.9.4' \
    'ffmpeg>=4.3.1' \
    'gcc' \
    'gdal' \
    'gdal>=2.4.1' \
    'geopandas' \
    'graphviz==6.0.1' \
    'h5py>=2.10.0' \
    'ipython>=7.16.1' \
    'ipywidgets==8.0.2' \
    'jsonschema>=3.2.0' \
    'jupyter' \
    'jupyter>=1.0.0' \
    'jupyter_console' \
    'jupyterlab-geojson==3.2.0' \
    'jupyterlab-git==0.39.2' \
    'jupyterlab-github==3.0.1' \
    'jupyterlab_pygments>=0.1.2' \
    'llvmlite' \
    'lz4-c>=1.9.3' \
    'matplotlib' \
    'mkl_fft>=1.3.0' \
    'mkl_random>=1.1.0' \
    'more-itertools' \
    'nbclient>=0.5.3' \
    'nc-time-axis==1.4.1' \
    'netcdf4>=1.4.2' \
    'notebook' \
    'numba' \
    'numpy' \
    'openpyxl>=3.0.9' \
    'pandas' \
    'pip' \
    'plotly==5.10.0' \
    'poppler>=0.67.0' \
    'py-xgboost==1.6.2' \
    'pygraphviz==1.10' \
    'pyresample' \
    'python-cdo>=1.4.0' \
    'python-graphviz==0.20.1' \
    'rarfile>=3.0' \
    'rasterio' \
    'rasterstats==0.17.0' \
    'rioxarray==0.12.0' \
    'scikit-learn>=0.24.2' \
    'scipy>=1.5.2' \
    'seaborn' \
    'testpath>=0.5.0' \
    'widgetsnbextension==4.0.3' \
    'wordcloud>=1.8.1' \
    'xcube==0.12.1' \
    'xarray==2022.6.0' \
    'xcube-cci==0.9.6' \
    'xcube-cds==0.9.1' \
    'xcube-sh==0.9.5' \
    'xcube_geodb==1.0.4' \
    'xlrd>=2.0.1'

RUN mamba update --update-all --yes

# Print a package list in case we need it for diagnostics or debugging.

RUN mamba list

RUN pip install \
    'pypro4sail @ git+https://github.com/hectornieto/pypro4sail@f6825f5b1325259cb014dcb934ccff2a9442a3ae' \
    'pyTSEB @ git+https://github.com/hectornieto/pyTSEB@9bb28da739090d36f9cc0c1a771efb897c05eb48' \
    'pytesmo' \
    'ismn'

# Copy the user init file to a location where it will be automatically run
# whenever a notebook is opened.

COPY init.py /home/jovyan/.ipython/profile_default/startup/init.py

# Set the default user and home directory. The environment variables are
# inherited from the base image which ultimately inherits them from
# base-notebook.

USER ${NB_UID}
WORKDIR "${HOME}"
