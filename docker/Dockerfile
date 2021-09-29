# We use a standard JupyterHub image as base. The original image is hosted on
# Docker Hub, but we use our own copy on quay.io, because Docker Hub's
# anonymous pull rate limits and quay.io's lack of support for pull
# credentials cause Docker-Hub-based builds to fail on quay.io; see
# https://issues.redhat.com/browse/PROJQUAY-1299?_sscc=t for details.

FROM quay.io/bcdev/scipy-notebook:2021-09-07

LABEL maintainer="pontus.lurcock@brockmann-consult.de"
LABEL name="avl-user-env"
LABEL version="1.0.1"
LABEL description="User environment for AVL JupyterHub deployment"

USER root

# The Jupyter images have mamba preinstalled and conda-forge as the default
# channel. Package versions are explicitly pinned to ensure a well-defined,
# reproducible environment.

RUN mamba install --quiet --yes \
    'xcube==0.9.0' \
    'xcube-sh==0.9.0' \
    'xcube-cci==0.9.0' \
    'xcube-cds==0.9.1' \
    'xcube_geodb==1.0.2' \
    'sentinelhub==3.3.2' \
    'rasterstats==0.15.0'

USER ${NB_UID}

WORKDIR "${HOME}"
