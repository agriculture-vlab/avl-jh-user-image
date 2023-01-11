[![Docker Repository on Quay](https://quay.io/repository/bcdev/avl-user/status "Docker Repository on Quay")](https://quay.io/repository/bcdev/avl-user)

# AVL user environment docker image configuration

This repository contains a Dockerfile defining an image that provides a custom
user environment for use in JupyterHub. The Dockerfile uses an Ubuntu image
as its base. Its content is based on a concatenation of Dockerfiles from
[Jupyter’s Docker Stacks collection](https://github.com/jupyter/docker-stacks),
specifically the stack `docker-stacks-foundation` – `base-notebook` –
`minimal-notebook` – `scipy-notebook`. Combining Dockerfile contents directly
like this is a less obvious approach than simply taking the `scipy-notebook`
image as a base, but it gives us direct control over installed software
versions and allows more customization and consolidation of build steps.
On top of the Docker Stacks content, the AVL user environment Dockerfile adds
some packages relevant to the AVL (xcube, etc.). It also adds an initialization
script under `/.ipython` which implements some AVL-specific configuration in
Python runtimes in notebooks. See
<https://zero-to-jupyterhub.readthedocs.io/en/latest/jupyterhub/customizing/user-environment.html>
for more details on custom user environments in JupyterHub.

The AVL user image is automatically rebuilt on every push to the repository
using the quay.io build service and made available in the Docker repository
`quay.io/bcdev/avl-user`. The quay.io web page for the Docker repository is at
<https://quay.io/repository/bcdev/avl-user>.

## Running the user image directly

While the AVL user image is intended for use within with AVL Jupyter Hub
deployment, it can also be run directly using docker, for example for testing
before deployment to a cluster:

```
docker run -p 8888:8888 quay.io/bcdev/avl-user:<tag>
```

Replace `<tag>` with a tag for the desired version of the image, and see the
`docker run` output for the URL of the JupyterLab environment. Note that there
are some differences between the deployed AVL and a locally running AVL user
image, since some additional configuration is carried out by Helm during
cluster deployment. In particular, when running the user image locally with
Docker, no environment variables are initialized with credentials for external
service access (e.g. geoDB), so if needed these must be set by the user (e.g.
with `os.environ['GEODB_AUTH_CLIENT_ID'] = '<my-client-id>'`, etc.).

## jupyterhub package versioning

The Jupyter hub process and single-user notebook server communicate using
an API provided by the `jupyterhub` package. For reliable operation, the hub and
user images in a deployment must use the same minor version of this package. You
can check the `jupyterhub` version in the user image with the following command:

```bash
docker run -it --rm quay.io/bcdev/avl-user:<tag> \
    python3 -c 'import jupyterhub; print(jupyterhub.__version__)'
```
