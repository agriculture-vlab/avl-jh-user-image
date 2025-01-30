## Changes in 4.0.1

* Update xcube_geodb package to 1.0.9 to maintain compatibility with new
  server version. (#26)

## Changes in 4.0.0

* Rewrite dockerfile based on revision 1c44e6d6e8f7 (2024-05-30) of the
  docker-stacks repository.
* Update jupyterhub package to v4.1.5 (corresponding to hub and chart
  version 3.3.7).
* Update all packages to latest versions.
* Update maintainer email address.
* Update notebook package from 6.5.2 to 7.2.1.
* Make an additional copy of the user ipython init file to /tmp, from where
  it can be copied at runtime even when another filesystem is mounted over
  /home.

## Changes in 3.1.1

* Revert jupyterhub version from 4.0.1 to 3.0.0, to match version in AVL
  Jupyter hub container image.

## Changes in 3.1.0

* Update Coiled package to 0.7.11 for compatibility with current server-side
  API.
* Add nbgitpuller, flox, and mkdocs packages.
* Update versions of many conda-forge packages.
* User lower case for value of cost-center tag on dask cluster.
* Make the new_cluster function use spot instances by default.
* Make the cost-center tag for Coiled clusters lower case.

## Changes in 3.0.0

* Rebase directly on an Ubuntu 20.04 image rather than the Docker Stacks
  scipy-notebook image.
* Incorporate all steps from the previously used Docker Stacks images into
  the AVL User Image Dockerfile itself.
* Update software versions.
* Note: there were no version 2 releases, except for beta versions; 3.0.0
  is the direct successor of 1.2.0.

## Changes in 1.2.0

* Add rsync and s3cmd packages.
* Update mamba version.
* Clean up mamba cache and ensure correct permissions after package
  installation.
* Don't do a full update of the conda environment (improves reproducibility).
* Add or update many packages (mostly requests for Land Training Course),
  including coiled.

## Changes in 1.1.5

* Update all apt and conda-forge packages to latest available versions when
  building the image.
* Adjust some package versions.
* Temporarily remove voila package due to incompatibility with recent
  ipywidgets versions.

## Changes in 1.1.4

* Add some more comments to dockerfile
* Update mamba to 0.25.0
* Update xcube packages: agriculture-vlab package to 0.20.0, xcube to 0.12.0,
  xcube_geodb to 1.0.4
* Update conda packages to latest versions
* Add the conda packages contextily, earthpy, and jupyterlab-github

## Changes in 1.1.3

* Use released versions of xcube (0.11.2) and xcube_geodb (1.0.3) rather than
  dev versions
* Use latest versions of xcube-cci (0.9.6) and xcube-sh (0.9.5)  

## Changes in 1.1.2

* Add a missing file.

## Changes in 1.1.1

* Add an ipython initialization script to predefine data stores in notebooks

## Changes in 1.1.0

* Use scipy-notebook:2021-11-01 as the base image, to ensure compatibility
  with chart version 1.2.0 and hub image version 1.2.0
* Add voila package

## Changes in 1.0.9

* Update base scipy-notebook image from 2021-09-27 to 2022-04-25
* Update version label from 1.0.8 to 1.0.9.dev0
* Remove all apt installs which were there to update insecure packages
  in the previous base image (but retain otb-bin and yarnpkg)
* Update mamba from 0.22.1 to 0.23.0
* Install current latest repository versions of xcube (6e37dec5ab36) and
  xcube_geodb (03803a7e39d9)
* Add plotly package
* Add nc-time-axis package

## Changes in 1.0.8

* Install conda packages as jovyan, not root
* Bump agriculture-vlab package from 0.1.0 to 0.1.1

## Changes in 1.0.7

* Update python3.8 to the newly-released 3.8.10-0ubuntu1~20.04.4

## Changes in 1.0.6

* xcube 0.10.2
* xcube-sh 0.9.4
* xcube-cci 0.9.5
* xcube-cds 0.9.1

## Changes in 1.0.5

* xcube 0.9.2
* xcube-sh 0.9.2
* xcube-cci 0.9.3
* xcube-cds 0.9.1

## Changes in 1.0.4

* xcube 0.9.1
* xcube-sh 0.9.1
* xcube-cci 0.9.0
* xcube-cds 0.9.1

## Changes in 1.0.3

* Add rioxarray conda package
