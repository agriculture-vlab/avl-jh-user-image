FROM jupyter/scipy-notebook:2021-09-07

LABEL maintainer="pontus.lurcock@brockmann-consult.de"
LABEL name=xcube-avl

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
