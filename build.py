import itertools
from jinja2 import Environment, FileSystemLoader
import os
import shutil
from helper import *

DIST = "dist"
REPO = "webplates/php"

VERSIONS = ["5.5", "5.6", "7.0"]
BUILDS = ["fpm"]
DISTROS = ["alpine"]

EXCLUSIONS = set(itertools.product(VERSIONS, ["apache"], ["alpine"]))

MATRIX = set(itertools.filterfalse(lambda x: x in EXCLUSIONS, itertools.chain(
    itertools.product(VERSIONS, BUILDS, [None]),
    itertools.product(VERSIONS, [None], DISTROS),
    itertools.product(VERSIONS, [None], [None]),
    itertools.product(VERSIONS, BUILDS, DISTROS)
)))

NODE = ["6.3.1"]

# Prepare Jinja
env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))))

# Clear the dist folder
if os.path.isdir(DIST):
    shutil.rmtree(DIST, ignore_errors=True)
os.mkdir(DIST)

paths = []
tags = []

# Build node containers
template = env.get_template('Dockerfile-node.template')

for element in MATRIX:
    for version in NODE:
        docker = template.render(parent=matrix_join(element, "-"), version=version, distro=element[2])
        path_elements = list(element)
        path_elements.extend(["node", minorize(version)])
        path = DIST + "/" + matrix_join(path_elements, "/") + "/"
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

delete_builds(REPO, token)
add_builds(REPO, token, paths, tags)

paths.insert(0, "PATH")
tags.insert(0, "TAG")
for c1, c2 in zip(paths, tags):
    print ("%-35s %s" % (c1, c2))
