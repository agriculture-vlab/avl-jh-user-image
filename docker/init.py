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
    account = 'bc'

    if provider == 'coiled':
        import coiled
        if software is None:
            # Construct an identifier from the current user image specifier.
            current_image = os.environ['JUPYTER_IMAGE']
            software = re.sub(
                '[:.]',
                '-',
                re.search(r'/([^/]+)$', current_image).group(1),
            )
            # If it doesn't exist yet, create it
            available_environments = coiled.list_software_environments(account=account).keys()
            if software not in available_environments:
                coiled.create_software_environment(
                    name=software,
                    container=current_image
                )
        
        return coiled.Cluster(
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
            account=account,
            # From config
            name=name,  # config 'coiled.name'
            software=software,  # config 'coiled.software'
            # Other
            **kwargs,
        )
    raise NotImplementedError(f'Unknown provider {provider!r}')
