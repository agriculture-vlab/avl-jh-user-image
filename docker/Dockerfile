# We use a standard JupyterHub image as base. The original image is hosted on
# Docker Hub, but we use our own copy on quay.io, because Docker Hub's
# recently-introduced anonymous pull rate limits and quay.io's lack of support
# for pull credentials cause Docker-Hub-based builds to fail on quay.io;
# see https://issues.redhat.com/browse/PROJQUAY-1299?_sscc=t for details.

FROM quay.io/bcdev/scipy-notebook:2021-09-07

LABEL maintainer="pontus.lurcock@brockmann-consult.de"
LABEL name="avl-user-env"
LABEL version="1.0.0"
LABEL description="User environment for AVL JupyterHub deployment"

USER root

# The Jupyter images have mamba preinstalled and conda-forge as the default
# channel.

RUN mamba install --quiet --yes \
    'xcube' \
    'xcube-sh' \
    'xcube-cci' \
    'xcube-cds' \
    'xcube_geodb' \
    'rasterstats'

USER ${NB_UID}

WORKDIR "${HOME}"
