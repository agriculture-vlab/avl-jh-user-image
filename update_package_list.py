#!/usr/bin/env python3

"""Update conda package versions for a dockerfile

Designed for use with the AVL user image dockerfile.

Motivation: we have a dockerfile that installs pinned package versions,
and we want to update the dockerfile to specify the latest available
versions of those packages (as far as inter-package compatibility allows).

This script takes a dockerfile containing installation commands of
the form:

RUN mamba install --quiet --yes \
    'agriculture-vlab==0.3.0' \
    'altair==5.0.1' \
    'beautifulsoup4==4.12.2' \
    'bokeh==3.2.0' \
    ...

It scrapes all the package names and versions, and constructs conda version
specifiers for the union set of all the installed packages, using the
pinned versions as minima -- producing something like:

    'agriculture-vlab>=0.3.0' \
    'altair>=5.0.1' \
    'beautifulsoup4>=4.12.2' \
    'bokeh>=3.2.0' \

The script runs `mamba create` with these minimum specifiers to create a conda
environment, then reads the list of package versions which were actually
installed. Finally, it prints out the original mamba installation snippets
from the dockerfile, but with the versions updated to the ones from the
newly created environment. These snippets can be manually checked and pasted
into the dockerfile in place of the previous package specifiers.

It's by no means guaranteed that every package will be upgraded to the latest
version -- e.g. if version 2.0.0 of pkg-a has updated its dependencies to
include `pkg-b<=2.0.0` then we clearly can't install version 2.0.0 of both
packages and mamba must pick one to prioritize.

The script supports a `--pin` option, which allows the user to specify
a comma-separated list of exact package versions. For instance, if the
latest xcube version is 1.1.2, the latest jupyterhub version is 4.0.1,
and the AVL Jupyter Hub image is currently using jupyterhub 3.0.0, you
might want to specify something like `--pin xcube=1.1.2,jupyterhub=3.0.0`:

 - `xcube=1.1.2` ensures that the latest xcube version will *definitely*
   be installed (if there is any valid way to do this), rather being
   kept back to allow the installation of a more recent version of some
   other package.

 - `jupyterhub=3.0.0` ensures that an *older* version of jupyterhub will
   be installed, to ensure compatibility with the version installed in
   the Hub image.
"""

import argparse
import re
import subprocess
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dockerfile", type=str)
    parser.add_argument("--pin", "-p", type=str)
    args = parser.parse_args()
    env_name = "temp2"
    pins = {
        spec.split("=")[0]: spec.split("=")[1] for spec in args.pin.split(",")
    }
    print("Pinning: ", pins)

    # Extract package name/version dicts from Dockerfile
    dict_list = get_package_dicts_from_dockerfile(args.dockerfile)

    # Create a union of the package dictionaries
    all_packages = {}
    for d in dict_list:
        for name in d:
            all_packages[name] = d[name]

    # Create >= environment from union list
    create_env(all_packages, env_name, pins)

    # Get versions of packages in environment
    new_versions = get_package_dict_from_env(env_name)

    for d in dict_list:
        for i, name in enumerate(d):
            suffix = "&& \\" if i == len(d) - 1 else "\\"
            print(f"    '{name}=={new_versions[name]}' {suffix}")
        print()


def get_package_dicts_from_dockerfile(dockerfile: str):
    with open(dockerfile, "r") as fh:
        lines = map(lambda s: s.strip(), fh.readlines())

    dict_list = []
    current_dict = None
    reading = False
    for line in lines:
        if reading:
            m = re.search("'(.*)==(.*)'", line)
            if m:
                current_dict[m.group(1)] = m.group(2)
            else:
                print("Warning: skipping " + line)
        if "&&" in line:
            reading = False
        if "RUN mamba install" in line:
            reading = True
            current_dict = {}
            dict_list.append(current_dict)

    return dict_list


def create_env(packages, env_name, pins):
    def spec(name):
        if name in pins:
            return f"{name}=={pins[name]}"
        else:
            return f"{name}>={packages[name]}"

    pkg_args = [spec(name) for name in packages]
    command = [
        "mamba",
        "create",
        "--name",
        env_name,
        "--channel",
        "conda-forge",
        "--yes",
    ] + pkg_args
    subprocess.run(command)


def get_package_dict_from_env(env_name):
    process = subprocess.run(
        ["mamba", "list", "--name", env_name, "--json"], capture_output=True
    )
    mamba_output = json.loads(process.stdout)
    package_dict = {elt["name"]: elt["version"] for elt in mamba_output}
    return package_dict


if __name__ == "__main__":
    main()
