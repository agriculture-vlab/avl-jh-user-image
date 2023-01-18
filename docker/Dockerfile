# Copyright Agriculture Virtual Laboratory Development Team and
# Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# This file originated as a concatenation of the Dockerfiles from
# docker-stacks-foundation, base-notebook, minimal-notebook, and scipy-notebook
# in https://github.com/jupyter/docker-stacks at revision a905ff6f6d7b.

# =========== docker-stacks-foundation

# https://hub.docker.com/_/ubuntu/
ARG ROOT_CONTAINER=ubuntu:20.04

FROM $ROOT_CONTAINER

LABEL maintainer="Agriculture Virtual Laboratory <support@agriculturevlab.eu>"
LABEL name="avl-user-env"
LABEL version="3.0.0"
LABEL description="User environment for AVL JupyterHub deployment"

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    # - apt-get upgrade is run to patch known vulnerabilities in apt-get packages as
    #   the ubuntu base image is rebuilt too seldom sometimes (less than once a month)
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    # - bzip2 is necessary to extract the micromamba executable.
    bzip2 \
    ca-certificates \
    locales \
    sudo \
    # - tini is installed as a helpful container entrypoint that reaps zombie
    #   processes and such of the actual executable we want to start, see
    #   https://github.com/krallin/tini#why-tini for details.
    tini \
    wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
# hadolint ignore=SC2016
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc && \
   # Add call to conda init script see https://stackoverflow.com/a/58081608/4413446
   echo 'eval "$(command conda shell.bash hook 2> /dev/null)"' >> /etc/skel/.bashrc

# Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd -l -m -s /bin/bash -N -u "${NB_UID}" "${NB_USER}" && \
    mkdir -p "${CONDA_DIR}" && \
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${HOME}" && \
    fix-permissions "${CONDA_DIR}"

USER ${NB_UID}

# Pin python version here, or set it to "default"
ARG PYTHON_VERSION=3.9

# Setup work directory for backward-compatibility
RUN mkdir "/home/${NB_USER}/work" && \
    fix-permissions "/home/${NB_USER}"

# Download and install Micromamba, and initialize Conda prefix.
#   <https://github.com/mamba-org/mamba#micromamba>
#   Similar projects using Micromamba:
#     - Micromamba-Docker: <https://github.com/mamba-org/micromamba-docker>
#     - repo2docker: <https://github.com/jupyterhub/repo2docker>
# Install Python, Mamba and jupyter_core
# Cleanup temporary files and remove Micromamba
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change
COPY --chown="${NB_UID}:${NB_GID}" initial-condarc "${CONDA_DIR}/.condarc"
WORKDIR /tmp
RUN set -x && \
    arch=$(uname -m) && \
    if [ "${arch}" = "x86_64" ]; then \
        # Should be simpler, see <https://github.com/mamba-org/mamba/issues/1437>
        arch="64"; \
    fi && \
    wget -qO /tmp/micromamba.tar.bz2 \
        "https://micromamba.snakepit.net/api/micromamba/linux-${arch}/latest" && \
    tar -xvjf /tmp/micromamba.tar.bz2 --strip-components=1 bin/micromamba && \
    rm /tmp/micromamba.tar.bz2 && \
    PYTHON_SPECIFIER="python=${PYTHON_VERSION}" && \
    if [[ "${PYTHON_VERSION}" == "default" ]]; then PYTHON_SPECIFIER="python"; fi && \
    # Install the packages
    ./micromamba install \
        --root-prefix="${CONDA_DIR}" \
        --prefix="${CONDA_DIR}" \
        --yes \
        "${PYTHON_SPECIFIER}" \
        'mamba' \
        'jupyter_core' && \
    rm micromamba && \
    # Pin major.minor version of python
    mamba list python | grep '^python ' | tr -s ' ' | cut -d ' ' -f 1,2 >> "${CONDA_DIR}/conda-meta/pinned" && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start.sh"]

# Copy local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"

# =============== base-notebook

ARG OWNER=jupyter

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    fonts-liberation \
    # - pandoc is used to convert notebooks to html files
    #   it's not present in aarch64 ubuntu image, so we install it here
    pandoc \
    # - run-one - a wrapper script that runs no more
    #   than one unique  instance  of  some  command with a unique set of arguments,
    #   we use `run-one-constantly` to support `RESTARTABLE` option
    run-one && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# Install Jupyter Notebook, Lab, and Hub
# Generate a notebook server config
# Cleanup temporary files
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change
WORKDIR /tmp
RUN mamba install --quiet --yes \
    'notebook==6.5.2' \
    'jupyterhub==3.0.0' \
    'jupyterlab==3.5.0' && \
    jupyter notebook --generate-config && \
    mamba clean --all -f -y && \
    npm cache clean --force && \
    jupyter lab clean && \
    rm -rf "/home/${NB_USER}/.cache/yarn" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

EXPOSE 8888

# Configure container startup
CMD ["start-notebook.sh"]

# Copy local files as late as possible to avoid cache busting
COPY start-notebook.sh start-singleuser.sh /usr/local/bin/
# Currently need to have both jupyter_notebook_config and jupyter_server_config to support classic and lab
COPY jupyter_server_config.py /etc/jupyter/

# Fix permissions on /etc/jupyter as root
USER root

# Legacy for Jupyter Notebook Server, see: [#1205](https://github.com/jupyter/docker-stacks/issues/1205)
RUN sed -re "s/c.ServerApp/c.NotebookApp/g" \
    /etc/jupyter/jupyter_server_config.py > /etc/jupyter/jupyter_notebook_config.py && \
    fix-permissions /etc/jupyter/

# HEALTHCHECK documentation: https://docs.docker.com/engine/reference/builder/#healthcheck
# This healtcheck works well for `lab`, `notebook`, `nbclassic`, `server` and `retro` jupyter commands
# https://github.com/jupyter/docker-stacks/issues/915#issuecomment-1068528799
HEALTHCHECK  --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -O- --no-verbose --tries=1 --no-check-certificate \
    http${GEN_CERT:+s}://localhost:8888${JUPYTERHUB_SERVICE_PREFIX:-/}api || exit 1

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"

# ================ minimal-notebook

ARG OWNER=jupyter

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for fully functional notebook server
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    # Common useful utilities
    git \
    nano-tiny \
    tzdata \
    unzip \
    vim-tiny \
    # git-over-ssh
    openssh-client \
    # less is needed to run help in R
    # see: https://github.com/jupyter/docker-stacks/issues/1588
    less \
    # nbconvert dependencies
    # https://nbconvert.readthedocs.io/en/latest/install.html#installing-tex
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    # Enable clipboard on Linux host systems
    xclip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create alternative for nano -> nano-tiny
RUN update-alternatives --install /usr/bin/nano nano /bin/nano-tiny 10

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

# Add R mimetype option to specify how the plot returns from R to the browser
COPY --chown=${NB_UID}:${NB_GID} Rprofile.site /opt/conda/lib/R/etc/

# ================== scipy-notebook and AVL additions

ARG OWNER=jupyter

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    # for cython: https://cython.readthedocs.io/en/latest/src/quickstart/install.html
    build-essential \
    # for latex labels
    cm-super \
    dvipng \
    # for matplotlib anim
    ffmpeg \
    rsync \
    s3cmd \
    yarnpkg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# Use the jovyan user for installs in the conda environment to avoid polluting
# it with files owned by root.

# Install Python 3 packages
# The py-xgboost package auto-selects the -cpu or -gpu variant on installation.
RUN mamba install --quiet --yes \
    'agriculture-vlab==0.2.1' \
    'altair==4.2.0' \
    'beautifulsoup4==4.11.1' \
    'bokeh==2.4.3' \
    'bottleneck==1.3.5' \
    'click==8.1.3' \
    'cloudpickle==2.2.0' \
    'coiled==0.2.59' \
    'conda-forge::blas=2.116=openblas' \
    'contextily==1.2.0' \
    'cython==0.29.33' \
    'dask-labextension==6.0.0' \
    'dask-ml==2022.5.27' \
    'dask==2022.12.1' \
    'dill==0.3.6' \
    'distributed==2022.12.1' \
    'earthpy==0.9.4' \
    'fsspec==2022.11.0' \
    'gcsfs==2022.11.0' \
    'graphviz==6.0.2' \
    'h5py==3.7.0' \
    'ipympl==0.9.2' \
    'ipywidgets==7.7.2' \
    # Temporary fix for: https://github.com/jupyter/docker-stacks/issues/1851
    'jupyter_server==2.0.6' \
    'jupyterlab-geojson==3.3.1' \
    'jupyterlab-git==0.41.0' \
    'jupyterlab-github==3.0.1' \
    'lz4==4.2.0' \
    'matplotlib-base==3.6.2' \
    'nb_conda_kernels==2.3.1' \
    'nc-time-axis==1.4.1' \
    'nodejs==18.12.1' \
    'numba==0.56.4' \
    'numexpr==2.8.3' \
    'numpy==1.23.5' \
    'openpyxl==3.0.10' \
    'pandas==1.5.2' \
    'patsy==0.5.3' \
    'pip==22.3.1' \
    'plotly==5.11.0' \
    'protobuf==4.21.12' \
    'py-xgboost==1.7.1' \
    'pyarrow==10.0.1' \
    'pygraphviz==1.10' \
    'pytables==3.7.0' \
    'python-graphviz==0.20.1' \
    'python-snappy==0.6.1' \
    'rasterstats==0.17.0' \
    'rioxarray==0.13.3' \
    's3fs==2022.11.0' \
    'scikit-image==0.19.3' \
    'scikit-learn==1.2.0' \
    'scipy==1.10.0' \
    'seaborn==0.12.2' \
    'sentinelhub==3.4.4' \
    'sqlalchemy==1.4.46' \
    'statsmodels==0.13.5' \
    'sympy==1.11.1' \
    'widgetsnbextension==3.6.1' \
    'xarray==2022.12.0' \
    'xcube-cci==0.9.7' \
    'xcube-cds==0.9.1' \
    'xcube-cmems==0.1.0' \
    'xcube-sh==0.10.0' \
    'xcube==0.12.1' \
    'xcube_geodb==1.0.4' \
    'xlrd==2.0.1' \
    'zarr==2.13.3' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Install facets which does not have a pip or conda package at the moment
WORKDIR /tmp
RUN git clone https://github.com/PAIR-code/facets.git && \
    jupyter nbextension install facets/facets-dist/ --sys-prefix && \
    rm -rf /tmp/facets && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME="/home/${NB_USER}/.cache/"

RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    fix-permissions "/home/${NB_USER}"

USER ${NB_UID}
WORKDIR "${HOME}"

# Copy the user init file into the home directory. The location corresponds
# to the default value of get_ipython().profile_dir.startup_dir in a
# z2jh deployment, but for such a deployment a persistent volume will in any
# case be mounted at the home directory so the original Dockerfile contents
# there will not be visible. Because of this, and because the startup_dir
# value may vary, deployments should make their own arrangements to ensure
# that the notebook runtime finds this init file or a copy of it.

COPY init.py /home/jovyan/.ipython/profile_default/startup/init.py

# Print a package list in case we need it for diagnostics or debugging.

RUN mamba list

