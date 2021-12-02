# We use a standard JupyterHub image as base. The original image is hosted on
# Docker Hub, but we use our own copy on quay.io, because Docker Hub's
# anonymous pull rate limits and quay.io's lack of support for pull
# credentials cause Docker-Hub-based builds to fail on quay.io; see
# https://issues.redhat.com/browse/PROJQUAY-1299?_sscc=t for details.

FROM quay.io/bcdev/scipy-notebook:2021-09-27

LABEL maintainer="pontus.lurcock@brockmann-consult.de"
LABEL name="avl-user-env"
LABEL version="1.0.5"
LABEL description="User environment for AVL JupyterHub deployment"

USER root


# Upgrade some packages to fix known vulnerabilities in the base image.

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    libcaca0=0.99.beta19-2.1ubuntu1.20.04.2 \
    libgcrypt20=1.8.5-5ubuntu1.1 \
    libicu66=66.1-2ubuntu2.1 \
    python3.8=3.8.10-0ubuntu1~20.04.1 \
    vim-tiny=2:8.1.2269-1ubuntu5.4 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# The Jupyter images have mamba preinstalled and conda-forge as the default
# channel. Package versions are explicitly pinned to ensure a well-defined,
# reproducible environment.

RUN mamba install --quiet --yes \
    'jupyterlab-geojson==3.1.2' \
    'jupyterlab-git==0.34.0' \
    'rasterstats==0.15.0' \
    'rioxarray==0.7.1' \
    'sentinelhub==3.3.2' \
    'xcube==0.9.2' \
    'xcube-cci==0.9.3' \
    'xcube-cds==0.9.1' \
    'xcube_geodb==1.0.2' \
    'xcube-sh==0.9.2'

USER ${NB_UID}

WORKDIR "${HOME}"
