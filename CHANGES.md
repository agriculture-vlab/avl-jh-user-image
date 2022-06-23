## Changes in 1.1.1

* Add an ipython initialization script to predefine data stores in notebooks.

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
