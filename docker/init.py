import os
from xcube.core.store import new_data_store

max_depth = 8

lab_store = new_data_store(
    "file",
    root="/home/jovyan/"
)
user_store = new_data_store(
    "s3",
    root=f"agriculture-vlab-user/{os.environ['JUPYTERHUB_USER']}/",
    max_depth=max_depth
)
scratch_store = new_data_store(
    "s3",
    root="agriculture-vlab-scratch/",
    max_depth=max_depth
)
test_store = new_data_store(
    "s3",
    root="agriculture-vlab-data-test",
    max_depth=max_depth
)
staging_store = new_data_store(
    "s3",
    root="agriculture-vlab-data-staging/",
    max_depth=max_depth
)
data_store = new_data_store(
    "s3",
    root="agriculture-vlab-data/",
    max_depth=max_depth
)
public_store_write = new_data_store(
    "s3",
    root=f"agriculture-vlab-public/{os.environ['JUPYTERHUB_USER']}/",
    max_depth=max_depth
)
public_store_read = new_data_store(
    "s3",
    root=f"agriculture-vlab-public/",
    max_depth=max_depth
)
