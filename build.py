import itertools
from jinja2 import Environment, FileSystemLoader
import os
import shutil
import semver

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
paths.insert(0, "PATH")
tags.sort()
tags.insert(0, "TAG")

for c1, c2 in zip(paths, tags):
    print ("%-35s %s" % (c1, c2))