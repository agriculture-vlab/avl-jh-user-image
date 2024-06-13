# Copyright Agriculture Virtual Laboratory Development Team and
# Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# This file originated as a concatenation of the Dockerfiles from
# docker-stacks-foundation, base-notebook, minimal-notebook, and scipy-notebook
# in https://github.com/jupyter/docker-stacks at revision 1c44e6d6e8f7
# (2024-05-30).

# The contents of docker-stacks-foundation and base-notebook are included
# almost verbatim, but package versions are pinned to make the build
# slightly more reproducible. (However, the apt-get update means that
# it's still not entirely reproducible.)

# =========== docker-stacks-foundation

# https://hub.docker.com/_/ubuntu/
ARG ROOT_CONTAINER=ubuntu:22.04

FROM $ROOT_CONTAINER

LABEL maintainer="Agriculture Virtual Laboratory <contact@agriculturevlab.eu>"
LABEL name="avl-user-env"
LABEL version="4.0.0"
LABEL description="User environment for AVL JupyterHub deployment"

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for the Server that starts
# but lacks all features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    # - `apt-get upgrade` is run to patch known vulnerabilities in system packages
    #   as the Ubuntu base image is rebuilt too seldom sometimes (less than once a month)
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    # - bzip2 is necessary to extract the micromamba executable.
    bzip2 \
    ca-certificates \
    locales \
    sudo \
    # - `tini` is installed as a helpful container entrypoint,
    #   that reaps zombie processes and such of the actual executable we want to start
    #   See https://github.com/krallin/tini#why-tini for details
    tini \
    wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    echo "C.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8
ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
# hadolint ignore=SC2016
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc && \
    # More information in: https://github.com/jupyter/docker-stacks/pull/2047
    # and docs: https://docs.conda.io/projects/conda/en/latest/dev-guide/deep-dives/activation.html
    echo 'eval "$(conda shell.bash hook)"' >> /etc/skel/.bashrc

# Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd --no-log-init --create-home --shell /bin/bash --uid "${NB_UID}" --no-user-group "${NB_USER}" && \
    mkdir -p "${CONDA_DIR}" && \
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

USER ${NB_UID}

# Pin the Python version here, or set it to "default"
ARG PYTHON_VERSION=3.11

# Setup work directory for backward-compatibility
RUN mkdir "/home/${NB_USER}/work" && \
    fix-permissions "/home/${NB_USER}"

# Download and install Micromamba, and initialize the Conda prefix.
#   <https://github.com/mamba-org/mamba#micromamba>
#   Similar projects using Micromamba:
#     - Micromamba-Docker: <https://github.com/mamba-org/micromamba-docker>
#     - repo2docker: <https://github.com/jupyterhub/repo2docker>
# Install Python, Mamba, and jupyter_core
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
    # https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#linux-and-macos
    wget --progress=dot:giga -O - \
        "https://micro.mamba.pm/api/micromamba/linux-${arch}/latest" | tar -xvj bin/micromamba && \
    PYTHON_SPECIFIER="python=${PYTHON_VERSION}" && \
    if [[ "${PYTHON_VERSION}" == "default" ]]; then PYTHON_SPECIFIER="python"; fi && \
    # Install the packages
    ./bin/micromamba install \
        --root-prefix="${CONDA_DIR}" \
        --prefix="${CONDA_DIR}" \
        --yes \
        "${PYTHON_SPECIFIER}" \
        'mamba' \
        'jupyter_core' && \
    rm -rf /tmp/bin/ && \
    # Pin major.minor version of python
    # https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html#preventing-packages-from-updating-pinning
    mamba list --full-name 'python' | tail -1 | tr -s ' ' | cut -d ' ' -f 1,2 | sed 's/\.[^.]*$/.*/' >> "${CONDA_DIR}/conda-meta/pinned" && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Copy local files as late as possible to avoid cache busting
COPY run-hooks.sh start.sh /usr/local/bin/

# Configure container entrypoint
ENTRYPOINT ["tini", "-g", "--", "start.sh"]

USER root

# Create dirs for startup hooks
RUN mkdir /usr/local/bin/start-notebook.d && \
    mkdir /usr/local/bin/before-notebook.d

COPY 10activate-conda-env.sh /usr/local/bin/before-notebook.d/

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"

# =============== base-notebook

ARG OWNER=jupyter

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for the Server that starts
# but lacks all features (e.g., download as all possible file formats)
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    # - Add necessary fonts for matplotlib/seaborn
    #   See https://github.com/jupyter/docker-stacks/pull/380 for details
    fonts-liberation \
    # - `pandoc` is used to convert notebooks to html files
    #   it's not present in the aarch64 Ubuntu image, so we install it here
    pandoc \
    # - `run-one` - a wrapper script that runs no more
    #   than one unique instance of some command with a unique set of arguments,
    #   we use `run-one-constantly` to support the `RESTARTABLE` option
    run-one && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# Install JupyterLab, Jupyter Notebook, JupyterHub and NBClassic
# Generate a Jupyter Server config
# Cleanup temporary files
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change

# TODO set nbclassic version
WORKDIR /tmp
RUN mamba install --quiet --yes \
    'jupyterlab==4.2.2' \
    'notebook==7.2.1' \
    # Make sure that the minor version of the jupyterhub package always \
    # matches the one in the hub image and the Helm chart's appVersion!
    'jupyterhub==4.1.5' \
    'nbclassic' && \
    jupyter server --generate-config && \
    mamba clean --all -f -y && \
    npm cache clean --force && \
    jupyter lab clean && \
    rm -rf "/home/${NB_USER}/.cache/yarn" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

ENV JUPYTER_PORT=8888
EXPOSE $JUPYTER_PORT

# Configure container startup
CMD ["start-notebook.py"]

# Copy local files as late as possible to avoid cache busting
COPY start-notebook.py start-notebook.sh start-singleuser.py start-singleuser.sh /usr/local/bin/
COPY jupyter_server_config.py docker_healthcheck.py /etc/jupyter/

# Fix permissions on /etc/jupyter as root
USER root
RUN fix-permissions /etc/jupyter/

# HEALTHCHECK documentation: https://docs.docker.com/engine/reference/builder/#healthcheck
# This healtcheck works well for `lab`, `notebook`, `nbclassic`, `server`, and `retro` jupyter commands
# https://github.com/jupyter/docker-stacks/issues/915#issuecomment-1068528799
HEALTHCHECK --interval=3s --timeout=1s --start-period=3s --retries=3 \
    CMD /etc/jupyter/docker_healthcheck.py || exit 1
# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"

# ================ minimal-notebook

ARG OWNER=jupyter

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for a fully functional Server
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    # Common useful utilities
    curl \
    git \
    nano-tiny \
    tzdata \
    unzip \
    vim-tiny \
    # git-over-ssh
    openssh-client \
    # `less` is needed to run help in R
    # see: https://github.com/jupyter/docker-stacks/issues/1588
    less \
    # `nbconvert` dependencies
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

# Add an R mimetype option to specify how the plot returns from R to the browser
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
    'agriculture-vlab>=0.3.0' \
    'altair>=5.0.1' \
    'beautifulsoup4>=4.12.2' \
    'bokeh>=3.2.0' \
    'bottleneck>=1.3.7' \
    'click>=8.1.3' \
    'cloudpickle>=2.2.1' \
    'coiled>=0.7.11' \
    'conda-forge::blas=2.117=openblas' \
    'contextily>=1.3.0' \
    'cython>=0.29.35' \
    'dask-labextension>=6.1.0' \
    'dask-ml>=2023.3.24' \
    'dask>=2023.6.1' \
    'dill>=0.3.6' \
    'distributed>=2023.6.1' \
    'earthpy>=0.9.4' \
    'flox>=0.7.2' \
    'fsspec>=2023.6.0' \
    'gcsfs>=2023.6.0' \
    'graphviz>=7.1.0' \
    'h5py>=3.8.0' \
    'ipympl>=0.9.3' \
    'ipywidgets>=8.0.6' \
    'jupyterlab-geojson>=3.4.0' \
    'jupyterlab-git>=0.41.0' \
    'jupyterlab-github>=3.0.1' \
    'lz4>=4.3.2' \
    'matplotlib-base>=3.7.1' \
    'mkdocs>=1.4.3' \
    'nb_conda_kernels>=2.3.1' \
    'nbgitpuller>=1.1.1' \
    'nc-time-axis>=1.4.1' \
    'nodejs>=18.15.0' \
    'numba>=0.57.1' \
    'numexpr>=2.8.4' \
    'numpy>=1.24.4' \
    'openpyxl>=3.1.2' \
    'pandas>=1.5.3' \
    'patsy>=0.5.3' \
    'pip>=23.1.2' \
    'plotly>=5.15.0' \
    'protobuf>=4.23.2' \
    'py-xgboost>=1.7.4' \
    'pyarrow>=12.0.0' \
    'pygraphviz>=1.10' \
    'pytables>=3.7.0' \
    'python-graphviz>=0.20.1' \
    'python-snappy>=0.6.1' \
    'rasterstats>=0.19.0' \
    'rioxarray>=0.14.1' \
    's3fs>=2023.6.0' \
    'scikit-image>=0.20.0' \
    'scikit-learn>=1.3.0' \
    'scipy>=1.11.1' \
    'seaborn>=0.12.2' \
    'sentinelhub>=3.9.1' \
    'sqlalchemy>=2.0.17' \
    'statsmodels>=0.14.0' \
    'sympy>=1.12' \
    'widgetsnbextension>=4.0.7' \
    'xarray>=2023.6.0' \
    'xcube-cci>=0.9.9' \
    'xcube-cds>=0.9.2' \
    'xcube-cmems>=0.1.2' \
    'xcube-sh>=0.10.3' \
    'xcube>=1.1.2' \
    'xcube_geodb>=1.0.6' \
    'xlrd>=2.0.1' \
    'zarr>=2.15.0' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Install facets package which does not have a `pip` or `conda-forge` package at the moment
WORKDIR /tmp
RUN git clone https://github.com/PAIR-code/facets && \
    jupyter nbclassic-extension install facets/facets-dist/ --sys-prefix && \
    rm -rf /tmp/facets && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Import matplotlib the first time to build the font cache
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
