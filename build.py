import itertools
from jinja2 import Environment, FileSystemLoader
import os
import shutil
import semver
import requests
import sys

VERSIONS = [5.5, 5.6, 7.0]
BUILDS = ["fpm"]
# BUILDS = ["apache", "fpm", "zts"]
DISTROS = ["alpine"]

MATRIX = set(itertools.product(VERSIONS, BUILDS, [None])) \
    .union(set(itertools.product(VERSIONS, [None], DISTROS))) \
    .union(set(itertools.product(VERSIONS, [None], [None]))) \
    .union(set(itertools.product(VERSIONS, BUILDS, DISTROS)))

EXCLUSIONS = set(itertools.product(VERSIONS, ["apache"], ["alpine"]))

MATRIX = MATRIX.difference(EXCLUSIONS)

NODE = ["6.3.1"]

env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))))

def matrix_join( matrix, separator ):
    valid_matrix = []
    for element in matrix:
        if not (element is None):
            valid_matrix.append(str(element))

    return separator.join(valid_matrix)

def delete_builds( token ):
    headers = {'Authorization': token}
    builds = [];

    response = requests.get("https://hub.docker.com/v2/repositories/webplates/php/autobuild/tags/", headers=headers)

    if response.status_code == 200:
        body = response.json()
        builds.extend(body["results"])

        while not (body["next"] is None):
            response = requests.get(body["next"], headers=headers)

            if response.status_code == 200:
                body = response.json()
                builds.extend(body["results"])
            else:
                raise Exception("Invalid response")
    else:
        raise Exception("Invalid response")

    for build in builds:
        requests.delete("https://hub.docker.com/v2/repositories/webplates/php/autobuild/tags/%s/" % (build["id"]), headers=headers)

def add_builds (token, paths, tags):
    headers = {'Authorization': token}

    for i in range(0, len(paths)):
        build = {"name": tags[i], "dockerfile_location": paths[i], "source_name": "master", "source_type": "Branch", "namespace": "webplates", "repoName": "php", "isNew": True}
        requests.post("https://hub.docker.com/v2/repositories/webplates/php/autobuild/tags/", headers=headers, data=build)

template = env.get_template('Dockerfile-node.template')

if os.path.isdir("dist"):
    shutil.rmtree("dist", ignore_errors=True)
os.mkdir("dist")

paths = []
tags = []

for element in MATRIX:
    for version in NODE:
        docker = template.render(parent=matrix_join(element, "-"), version=version, distro=element[2])
        path_elements = list(element)
        version_info = semver.parse(version)
        path_elements.extend(["node", str(version_info["major"]) + "." + str(version_info["minor"])])
        path = "dist/" + matrix_join(path_elements, "/") + "/"
        dockerfile = path + "Dockerfile"
        os.makedirs(os.path.dirname(dockerfile), exist_ok=True)
        with open(dockerfile, "w") as f:
            f.write(docker)
        paths.append(path);
        tags.append(matrix_join(path_elements, "-"));

paths.sort()
tags.sort()

with open(".auth", "r") as f:
    token = f.readline().rstrip()

delete_builds(token)
add_builds(token, paths, tags)

paths.insert(0, "PATH")
tags.insert(0, "TAG")
for c1, c2 in zip(paths, tags):
    print ("%-35s %s" % (c1, c2))
