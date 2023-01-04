import os
import re
from xcube.core.store import new_data_store
import distributed.deploy
from typing import Optional

max_depth = 8

lab_store = new_data_store("file", root="/home/jovyan/")
user_store = new_data_store(
    "s3",
    root=f"agriculture-vlab-user/{os.environ['JUPYTERHUB_USER']}/",
    max_depth=max_depth,
)
scratch_store = new_data_store(
    "s3", root="agriculture-vlab-scratch/", max_depth=max_depth
)
test_store = new_data_store(
    "s3", root="agriculture-vlab-data-test", max_depth=max_depth
)
staging_store = new_data_store(
    "s3", root="agriculture-vlab-data-staging/", max_depth=max_depth
)
data_store = new_data_store(
    "s3", root="agriculture-vlab-data/", max_depth=max_depth
)
public_store_write = new_data_store(
    "s3",
    root=f"agriculture-vlab-public/{os.environ['JUPYTERHUB_USER']}/",
    max_depth=max_depth,
)
public_store_read = new_data_store(
    "s3", root=f"agriculture-vlab-public/", max_depth=max_depth
)


def new_cluster(
    provider: str = 'coiled',
    name: Optional[str] = None,
    software: str = None,
    n_workers: int = 4,
    **kwargs,
) -> distributed.deploy.Cluster:
    if software is None:
        # Construct an identifier from the current user image specifier.
        software = re.sub(
            '[:.]',
            '-',
            re.search(r'/([^/]+)$', os.environ['JUPYTER_IMAGE']).group(1),
        )
    if provider == 'coiled':
        from coiled import Cluster

        return Cluster(
            # No config (see ~/.config/dask/coiled.yml)
            n_workers=n_workers,
            environ=None,  # Pass credentials to workers?
            tags={
                'cost-center': 'AVL',
                'environment': 'dev',
                'creator': 'auto',
                'purpose': 'AVL dask cluster',
            },
            # From login
            account='bc',
            # From config
            name=name,  # config 'coiled.name'
            software=software,  # config 'coiled.software'
            # Other
            **kwargs,
        )
    raise NotImplementedError(f'Unknown provider {provider!r}')
